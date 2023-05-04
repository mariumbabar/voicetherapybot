from tkinter import *
from chat2 import get_response, bot_name
import threading
import speech_recognition as sr


class ChatApplication:
    
    def __init__(self):
        self.window = Tk()
        self._setup_main_window()
        
    def run(self):
        self.window.mainloop()
        
    def _setup_main_window(self):
        self.window.title("Chat")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=470, height=550, bg="#17202A")
        
        # head label
        head_label = Label(self.window, bg="#17202A", fg="#EAECEE",
                           text="Welcome", font="Helvetica 13 bold", pady=10)
        head_label.place(relwidth=1)
        
        # tiny divider
        line = Label(self.window, width=450, bg="#ABB2B9")
        line.place(relwidth=1, rely=0.07, relheight=0.012)
        
        # text widget
        self.text_widget = Text(self.window, width=20, height=2, bg="#17202A", fg="#EAECEE",
                                font="Helvetica 14", padx=5, pady=5)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED)
        
        # scroll bar
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text_widget.yview)
        
        # bottom label
        bottom_label = Label(self.window, bg="#ABB2B9", height=80)
        bottom_label.place(relwidth=1, rely=0.825)
        
        # start listening for voice input in a separate thread
        threading.Thread(target=self._listen_for_input).start()
        
    def _listen_for_input(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            while True:
                audio = r.listen(source)

                try:
                    msg = r.recognize_google(audio)
                    self._insert_message(msg, "You")
                except sr.UnknownValueError:
                    print("Could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))
        
    def _insert_message(self, msg, sender):
        if not msg:
            return
        
        msg1 = f"{sender}: {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)
        
        msg2 = f"{bot_name}: {get_response(msg)}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg2)
        self.text_widget.configure(state=DISABLED)
        
        self.text_widget.see(END)
             
        
if __name__ == "__main__":
    app = ChatApplication()
    app.run()
