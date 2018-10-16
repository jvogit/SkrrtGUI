from tkinter import *
from tkinter import ttk

class FocusModeGUI(ttk.Frame):

    def __init__(self, root, parent, app, **args):
        self.app = app
        super().__init__(parent, **args)
        print("Initialized FocusMode GUI")
        self.create_widgets()
        self.grid_widgets()
        
    def create_widgets(self):
        self.statusBar = Label(self, width=94, height=5, relief='groove', textvariable=self.app.statusVar)
        self.speedometer = Label(self, width = 30, height=26, relief='groove', textvariable=self.app.speedVar)
    def grid_widgets(self):
        self.statusBar.grid(column=0, row = 0, sticky='NEWS')
        self.speedometer.grid(column=0, row=1, sticky='NEWS')
        pass
