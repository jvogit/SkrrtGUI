from tkinter import *
from tkinter import ttk

class FocusModeGUI(ttk.Frame):
    def __init__(self, root, parent, app, **args):
        self.app = app
        super().__init__(parent, **args)
        print("Initialized FocusMode GUI")
        self.pixel = PhotoImage(width=30, height=25)
        self.create_widgets()
        self.grid_widgets()
        
    #width 94 height 31 !
    def create_widgets(self):
        self.statusBar = Label(self, width=90, height=5, relief='groove', textvariable=self.app.statusVar)
        self.batteryInfo = Label(self, font=('Courier', 15),width=10, height=1, justify='center', textvariable=self.app.batteryInfoVar)
        self.cInd = Label(self, width=3, height=5, textvariable=self.app.lightningVar)
        self.revert = Button(self, width=30, height=8, relief='flat', text='', command=self.app.switchFrame)
        self.left_revert = Button(self, width=30, height=8, relief='flat', text='', command=self.app.switchFrame)
        self.speed = Label(self, font=('Courier', 60), width=3, height=1, textvariable=self.app.speedVar)
        self.placeholder1 = Button(self, width=30, height=8, relief='flat', state=DISABLED)
        self.placeholder2 = Button(self, width=30, height=8, relief='flat', state=DISABLED)
        self.placeholder3 = Button(self, width=30, height=8, relief='flat', state=DISABLED)
        
    def grid_widgets(self):
        self.statusBar.grid(column=0, row = 0, columnspan=3, sticky='news')
        self.placeholder1.grid(column=0, row=1, sticky='news')
        self.placeholder2.grid(column=1, row=2, sticky='news')
        self.placeholder3.grid(column=2, row=3, sticky='news')
        self.revert.grid(column=2, row=1, rowspan=3, sticky='news')
        self.revert.tkraise()
        self.left_revert.grid(column=0, row=1, rowspan=3, sticky='news')
        self.left_revert.tkraise()
        self.speed.grid(column=1, row=1, rowspan=3, sticky='news')
        self.batteryInfo.grid(column=1, row=3, sticky='news')
        self.cInd.grid(column=1, row=3, sticky='e')
        self.speed.tkraise()
        self.batteryInfo.tkraise()
        self.cInd.tkraise()
        pass
