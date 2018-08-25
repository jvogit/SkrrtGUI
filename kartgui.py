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
        root["bg"] = 'black'
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
        self.statusVar = StringVar(self, value="OFF")
        self.onoff = StringVar(self, value="ON")
        self.kart = Kart()
        
    def toggleFullScreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)
        
    def create_widgets(self):
        self.onButton = Button(self, textvariable=self.onoff, height=24, width=30, command=self.prompt)
        self.forward = Button(self, text="Forward", height=8, width=30, state=DISABLED, command=lambda : self.statusVar.set("Forward"))
        self.neutral = Button(self, text="Neutral", height=8, width=30, state=DISABLED, command=lambda : self.statusVar.set("Neutral"))
        self.reverse = Button(self, text="Reverse", height=8, width=30, state=DISABLED, command=lambda : self.statusVar.set("Reverse"))
        self.batteryToggleButton = Button(self, text="Battery Pack", height=8, width=30)
        self.status = Label(self, width=90, height=5, textvariable=self.statusVar, relief='groove')
        self.speedDisplay = Label(self, width=30, height=8, relief='groove', text='0')
        
    def grid_widgets(self):
        self.status.grid(column=0, row=0, columnspan=3, sticky='NEWS')
        self.speedDisplay.grid(column=2, row=1, sticky='NWES', rowspan=2)
        self.onButton.grid(column=0, row=1, rowspan=3, sticky='NEWS')
        self.forward.grid(column=1, row=1, sticky='NWES')
        self.neutral.grid(column=1, row=2, sticky='NWES')
        self.reverse.grid(column=1, row=3, sticky='NWES')
        self.batteryToggleButton.grid(column=2, row=3, sticky='NWES')
        for i in range(3):
            self.root.grid_columnconfigure(i, weight=1)
            self.root.grid_rowconfigure(i, weight=1)
            
    def prompt(self):
        onoff=self.onoff.get()
        if onoff == "OFF" or mb.askyesno(message='Check your surroundings.\nReady to go?', master=self.root):
            if(onoff == 'ON'):
                self.onoff.set("OFF")
                self.kart.on(self)
            else:
                self.onoff.set("ON")
                self.kart.off(self)
        else:
            pass

    def disableButton(self, button):
        button.config(state=DISABLED)
    def enableButton(self, button):
        button.config(state=NORMAL)

class Kart:

    def on(self, app):
        app.statusVar.set("ON")
        root = app.root
        app.disableButton(app.onButton)
        root.after(1000, lambda : app.enableButton(app.forward))
        root.after(1000, lambda : app.enableButton(app.reverse))
        root.after(1000, lambda : app.enableButton(app.onButton))
    def off(self, app):
        app.statusVar.set("OFF")
        app.disableButton(app.forward)
        app.disableButton(app.reverse)

if __name__ == '__main__':
    Application.main()
