from tkinter import *
from tkinter import ttk
import threading
from siricontrol import Control
import videomyguy
#Application class
class Application(ttk.Frame):

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
        self.create_widgets()
        self.grid_widgets()
        SiriListenThread(self).start()
    
    def create_widgets(self):
        self.textVar = StringVar(self, value='Test')
        self.label = Label(self, width = 30, height = 30, textvariable=self.textVar)
        pass #means do nothing

    def grid_widgets(self):
        self.label.grid(column=0, row = 0)
        pass #I put this here to prevent compilation errors. Also indicates WIP

    #'self' argument to use class instance. equivalent to 'this' in java
    def create_variables(self):
        self.someVar = 'Hello, World!' #setting class instance variables
        pass

    def take_me_home(self):
        videomyguy.PlayVideo('sample.mp4')

class SiriListenThread(threading.Thread):
    def __init__(self, gui):
        super().__init__()
        self.gui = gui

    def run(self):
        Control(self.gui)
#Allows start
if __name__ == "__main__":
    Application.main()
