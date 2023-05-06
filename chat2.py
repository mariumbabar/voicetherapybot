import json
import random
import speech_recognition as sr
import torch
from gtts import gTTS
from playsound import playsound

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Aira"

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        message = r.recognize_google(audio)
        return message
    except sr.UnknownValueError:
        return "I'm sorry, I did not understand what you said"
    except sr.RequestError:
        return "Sorry, I'm having trouble accessing the speech recognition service"

def get_response(msg):
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                response = random.choice(intent['responses'])
                # Use gTTS to convert text to audio and save it to a file
                tts = gTTS(response)
                tts.save('response.mp3')
                # Use playsound to play the audio file
                playsound('response.mp3')
                return response

    response = "I do not understand..."
    # Use gTTS to convert text to audio and save it to a file
    tts = gTTS(response)
    tts.save('response.mp3')
    # Use playsound to play the audio file
    playsound('response.mp3')
    return response

if __name__ == "__main__":
    print("Start talking with the bot (say 'bye' or 'quit' to stop)!")
    while True:
        message = get_audio()
        if message:
            if message.lower() in ["bye", "quit"]:
                print("Goodbye!")
                break
            print("You: " + message)
            response = get_response(message)
            print(bot_name + ": " + response)
        else:
            print("I'm sorry, I did not understand what you said")
