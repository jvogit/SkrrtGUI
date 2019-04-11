from tkinter import *
import threading
from siricontrol import Control
from KartSiriControlModule import *
from PIL import Image, ImageTk
from pathlib import Path
from audioplayer import AudioPlayer
import time
import gtts
from gtts import gTTS
import hashlib
#Application class
class Application(Frame):

    someVar = 'Default' #Setting class variables
    
    @classmethod
    def main(cls):
        #Set up your root and initial settings here!
        NoDefaultRoot()
        root = Tk()
        
        app = cls(root)
        app.grid(column=0, row=0)
        root.geometry("800x800")
        root.mainloop()

    def __init__(self, root, **args):
        super().__init__(root, **args)
        print("Initialize Application")
        #Set up applicatiom variables, create widgets, grid widgets onto main frame
        self.root = root
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.audioplayer = AudioPlayer()
        self.create_widgets()
        self.grid_widgets()
        self.thread = SiriListenThread(KartSiriControlModule(self))
        self.thread.start()
    
    def create_widgets(self):
        self.textVar = StringVar(self, value='Oh boy')
        self.label = Label(self, textvariable=self.textVar)
        self.button = Button(self, text='STOP', command=self.audioplayer.stop)
        pass #means do nothing

    def grid_widgets(self):
        self.label.grid(column=0, row = 0)
        self.button.grid(column=0, row=1)
        pass #I put this here to prevent compilation errors. Also indicates WIP

    #'self' argument to use class instance. equivalent to 'this' in java
    def create_variables(self):
        self.someVar = 'Hello, World!' #setting class instance variables
        pass

    def guess_who_here(self):
        img = ImageTk.PhotoImage(Image.open('patrick.jpg'), master=self.root)
        self.root.after(2000, lambda : self.label.config(image = img))
        self.audioplayer.PlayVideo('sample2.mp3')

    def play_song(self, to):
        print('trying to  loop up : ' + to)
        self.audioplayer.LookUpAndPlay(to, False, self.tts)

    def on_closing(self):
        print('Closed')
        self.thread.stop()
        self.audioplayer.stop()
        self.root.destroy()

    def tts(self, tosay):
        encoded = hashlib.sha224(tosay.encode()).hexdigest()
        dire = Path("tts")
        file = Path("tts/"+encoded + ".mp3")
        if not dire.exists():
            dire.mkdir()
        if not file.is_file():
            gTTS(tosay, lang='en').save("tts/"+encoded + ".mp3")
        self.audioplayer.inde_play("tts/"+encoded+".mp3")

#Allows start
if __name__ == "__main__":
    '''print(gtts.lang.tts_langs())
    while True:
        pass'''
    app = Application.main()
