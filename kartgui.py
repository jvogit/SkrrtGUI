from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb

class Application(ttk.Frame):
    
    @classmethod
    def main(cls):
        NoDefaultRoot()
        root = Tk()
        app = cls(root)
        app.grid(column=1, row=1)
        root.resizable(True, True)
        root.geometry("800x480")
        #root.attributes("-fullscreen", True)
        root.bind("<F11>", app.toggleFullScreen)
        root.mainloop()
        
    def __init__(self, root, **args):
        super().__init__(root, **args)
        print("Initialized application")
        self.root = root
        self.create_variables()
        self.create_widgets()
        self.grid_widgets()
        
    def create_variables(self):
        self.fullscreen = True
        self.statusVar = StringVar(self, value="")
        self.onoff = StringVar(self, value="ON")
        
    def toggleFullScreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)
        
    def create_widgets(self):
        self.but1 = Button(self, textvariable=self.onoff, height=24, width=30, command=self.prompt)
        self.but2 = Button(self, text="Forward", height=8, width=30, command=lambda : self.statusVar.set("Forward"))
        self.but3 = Button(self, text="NITROUS", height=8, width=30, command=lambda : self.statusVar.set("BOOST"))
        self.status = Label(self, width=90, textvariable=self.statusVar, relief='groove')
        
    def grid_widgets(self):
        self.status.grid(column=0, row=0, columnspan=3, sticky='NEWS')
        self.but1.grid(column=0, row=1, rowspan=3, sticky='N')
        self.but2.grid(column=1, row=1, sticky='N')
        self.but3.grid(column=2, row=1, sticky='N')
        for i in range(3):
            self.root.grid_columnconfigure(i, weight=1)
            self.root.grid_rowconfigure(i, weight=1)
            
    def prompt(self):
        onoff=self.onoff.get()
        if onoff == "OFF" or mb.askyesno(message='Check your surroundings.\nReady to go?', master=self.root):
            if(onoff == 'ON'):
                self.onoff.set("OFF")
            else:
                self.onoff.set("ON")
        else:
            pass
        
if __name__ == '__main__':
    Application.main()
