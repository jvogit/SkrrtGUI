from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import threading
import time

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
        root.protocol("WM_DELETE_WINDOW", app.on_closing)
        root.mainloop()
        
    def __init__(self, root, **args):
        super().__init__(root, **args)
        print("Initialized application")
        self.root = root
        self.create_variables()
        self.create_threads()
        self.create_widgets()
        self.grid_widgets()
        self.speedometerThread.start()
        
    def create_variables(self):
        self.fullscreen = True
        self.statusVar = StringVar(self, value="OFF")
        self.onoff = StringVar(self, value="ON")
        self.speedVar = StringVar(self, value="0\nmph")
        self.kart = Kart()
        
    def toggleFullScreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)

    def create_threads(self):
        self.threadingEvent = threading.Event()
        self.speedometerThread = SpeedometerThread(self)
    
    def create_widgets(self):
        self.onButton = Button(self, textvariable=self.onoff, height=24, width=30, command=self.prompt)
        self.forward = Button(self, text="Forward", height=8, width=30, state=DISABLED, command=lambda : self.kart.forward(self))
        self.neutral = Button(self, text="Neutral", height=8, width=30, state=DISABLED, command=lambda : self.kart.neutral(self))
        self.reverse = Button(self, text="Reverse", height=8, width=30, state=DISABLED, command=lambda : self.kart.reverse(self))
        self.batteryToggleButton = Button(self, text="Switch Battery Pack", height=8, width=30)
        self.status = Label(self, width=90, height=5, textvariable=self.statusVar, relief='groove')
        self.speedDisplay = Label(self, width=30, height=15, relief='groove', textvariable=self.speedVar)
        self.batteryChargingDisplay = Label(self, width = 30, height = 2, relief='groove', text='Battery Pack {0} Charging')
        
    def grid_widgets(self):
        self.status.grid(column=0, row=0, columnspan=3, sticky='NEWS')
        self.speedDisplay.grid(column=2, row=1, sticky='NEW', rowspan=2)
        self.batteryChargingDisplay.grid(column=2, row=2, sticky='EWS')
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

    def on_closing(self):
        print("Application terminated")
        self.root.destroy()
        self.threadingEvent.set()

    @staticmethod
    def disableButton(*buttons):
        for button in buttons:
            button.config(state=DISABLED)

    @staticmethod
    def enableButton(*buttons):
        for button in buttons:
            button.config(state=NORMAL)

class Kart:

    def __init__(self):
        self.forwardBool = False;
        self.neutralBool = False;
        self.reverseBool = False;
    
    def on(self, app):
        app.statusVar.set("Turning on . . .")
        root = app.root
        Application.disableButton(app.onButton)
        root.after(1000, lambda : Util.batch_execute_func(Application.enableButton(app.neutral, app.onButton), \
                                                          app.statusVar.set("On"), \
                                                          app.neutral.invoke()))
    def off(self, app):
        app.statusVar.set("OFF")
        Application.disableButton(app.forward, app.neutral, app.reverse, app.onButton)
        app.root.after(1000, lambda : Application.enableButton(app.onButton))

    def forward(self, app):
        Application.disableButton(app.forward, app.reverse, app.onButton)
        app.root.after(1000, lambda : Util.batch_execute_func(Application.enableButton(app.neutral, app.onButton), \
                                                              app.statusVar.set("Forward")))
        pass

    def neutral(self, app):
        Application.disableButton(app.neutral, app.onButton)
        app.root.after(1000, lambda : Util.batch_execute_func(Application.enableButton(app.onButton, app.forward, app.reverse), \
                                                              app.statusVar.set("Neutral")))
        pass

    def reverse(self, app):
        Application.disableButton(app.reverse, app.forward, app.onButton)
        app.root.after(1000, lambda : Util.batch_execute_func(Application.enableButton(app.onButton, app.neutral), \
                                                              app.statusVar.set("Reverse")))
        
        pass

class SpeedometerThread(threading.Thread):
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.app = app
        self.name = "Speedometer"
        self.counter = 0;
        self.exitFlag = 0;

    def run(self):
        while True and self.exitFlag == 0:
            if self.counter < 200:
                self.counter += 1
                self.app.speedVar.set(str(self.counter)+"\nmph")
                #time.sleep(1)
                if self.app.threadingEvent.wait(timeout=1):
                    break
            else:
                print("Max speed!")
        print(self.name + " thread exited gracefully!")

class Util:
    
    @staticmethod
    def batch_execute_func(*funcs):
        for f in funcs:
            f

if __name__ == '__main__':
    Application.main()
