from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
from Speedometer import Speedometer
from FocusModeGUI import FocusModeGUI
import threading
import time
import math
import json
import os
import RPi.GPIO as GPIO
import KartSerialConnector as serial

class Application(ttk.Frame):
    
    @classmethod
    def main(cls):
        def load_config():
            default_config = json.dumps({"sirisys":False},
                            indent=4, sort_keys=True)
            try:
                config = open(os.path.join(os.path.dirname(__file__), "config.txt"), "r")
            except OSError:
                config = open(os.path.join(os.path.dirname(__file__), "config.txt"), "w+")
                config.write(default_config)
            config.seek(0)
            loaded = json.loads(config.read())
            config.close()
            return loaded
        loaded = load_config()
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        root = Tk()
        root.geometry("800x480")
        root.resizable(True, True)
        container = ttk.Frame(root)
        container.grid(column=1, row=1)
        app = cls(root, container, loaded)
        frames = [app, FocusModeGUI(root, container, app)]
        frames[0].grid(column=1,row=1)
        frames[1].grid(column=1,row=1)
        frames[0].tkraise()
        app.frames = frames
        #app.grid(column=1, row=1)
        root["bg"] = 'black'
        #root.attributes("-fullscreen", True)
        root.bind("<F11>", app.toggleFullScreen)
        root.protocol("WM_DELETE_WINDOW", app.on_closing)
        root.mainloop()
    
    def __init__(self, root, parent, config, **args):
        super().__init__(parent, **args)
        print("Initialized application")
        self.root = root
        self.config = config
        self.frames = []
        self.frameOn = 0
        self.create_variables()
        self.create_threads()
        self.create_widgets()
        self.grid_widgets()
        self.speedometerThread.start()
        self.batteryVoltageThread.start()
        
    def switchFrame(self):
        if(self.frameOn == 0):
            self.switchFrameOn(1)
        else:
            self.switchFrameOn(0)

    def switchFrameOn(self, to):
        self.frames[to].tkraise()
        self.frameOn = to
        
    def create_variables(self):
        self.fullscreen = True
        self.statusVar = StringVar(self, value="OFF")
        self.onoff = StringVar(self, value="ON")
        self.speedVar = StringVar(self, value="0\nmph")
        self.batteryInfoVar = StringVar(self, value = 'Battery Pack {0}\n{1}% {2}V ⚡')
        self.lightningVar = StringVar(self, value = '\n\n')
        self.kart = Kart()
        
    def toggleFullScreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)

    def init_siri_sys(self):
        if(not self.config["sirisys"]):
            return
        try:
            import scs.KartSiriControlModule as kscm
        except Exception as e:
            print(e)
            return
        self.kartSiri = kscm.KartSiriControlModule(self)
        self.siriThread = kscm.SiriListenThread(self.kartSiri)
        self.siriThread.start()
        
    
    def create_threads(self):
        self.speedometerThread = SpeedometerThread(self)
        self.batteryVoltageThread = BatteryVoltageThread(self)
        self.init_siri_sys()
    
    def create_widgets(self):
        self.onButton = Button(self, textvariable=self.onoff, height=24, width=30, command=self.prompt)
        self.forward = Button(self, text="Forward", height=8, width=30, state=DISABLED, command=lambda : self.kart.forward(self))
        self.neutral = Button(self, text="Neutral", height=8, width=30, state=DISABLED, command=lambda : self.kart.neutral(self))
        self.reverse = Button(self, text="Reverse", height=8, width=30, state=DISABLED, command=lambda : self.kart.reverse(self))
        self.focusModeButton = Button(self, text="FOCUS MODE", relief='flat', height=4, width=30, command=lambda : self.switchFrame())
        self.status = Label(self, width=90, height=5, textvariable=self.statusVar, relief='groove')
        self.speedDisplay = Label(self, width=30, height=15, relief='flat', textvariable=self.speedVar)
        self.batteryChargingDisplay = Label(self, width = 30, height = 2, textvariable=self.batteryInfoVar)
        self.gasChange = Button(self, text="Gas", height=4, width=30, relief='flat', command=lambda : self.kart.gas(self))
        self.lightningDisplay = Label(self, width = 3, height = 2, textvariable=self.lightningVar)
        
    def grid_widgets(self):
        self.status.grid(column=0, row=0, columnspan=3, sticky='NEWS')
        self.speedDisplay.grid(column=2, row=1, sticky='NEW', rowspan=2)
        self.batteryChargingDisplay.grid(column=2, row=2, sticky='EWS')
        self.onButton.grid(column=0, row=1, rowspan=3, sticky='NEWS')
        self.forward.grid(column=1, row=1, sticky='NWES')
        self.neutral.grid(column=1, row=2, sticky='NWES')
        self.reverse.grid(column=1, row=3, sticky='NWES')
        self.focusModeButton.grid(column=2, row=3, sticky='NWE')
        self.lightningDisplay.grid(column=2, row=2, sticky='ES')
        self.gasChange.grid(column=2, row=3, sticky='EWS')
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
        try:
            self.kart.off(self)
            self.speedometerThread.event.set()
            self.batteryVoltageThread.event.set()
            self.siriThread.stop()
        except Exception as e:
            print(e)
            pass
        self.root.destroy()
        GPIO.cleanup()

    @staticmethod
    def disableButton(*buttons):
        for button in buttons:
            button.config(state=DISABLED)

    @staticmethod
    def enableButton(*buttons):
        for button in buttons:
            button.config(state=NORMAL)

class Kart:
    """
    gpio pins 36-40 even, 29-37 odd
    29 - power/keyswitch
    31 - enable
    35 - reverse
    37 - forward
    40 - hall
    """
    pins = [29, 31, 35, 37, 11, 13]
    DEFAULT_PIN_DELAY = 0.05
    FULL_OFF_DELAY = int(len(pins) * 0.05) + 1
    SAFETY_OFF_DELAY = FULL_OFF_DELAY + 3
    bat_one = False
    
    def __init__(self):
        GPIO.setup(self.pins, GPIO.OUT)
        GPIO.setup([38, 40], GPIO.OUT)
        self.forwardBool = False;
        self.neutralBool = False;
        self.reverseBool = False;
    
    def on(self, app):
        self.switch_battery(app, False)
        app.statusVar.set("Turning on . . .")
        root = app.root
        Application.disableButton(app.onButton, app.gasChange)
        root.after(1, lambda : Util.batch_execute_func(Application.enableButton(app.neutral, app.onButton, app.gasChange), \
                                                            app.statusVar.set("ON"), \
                                                            app.onoff.set("OFF"),\
                                                            app.neutral.invoke()\
                                                          ))
    def off(self, app):
        app.statusVar.set("Turning off. . .")
        Application.disableButton(app.forward, app.neutral, app.reverse, app.onButton, app.gasChange)
        app.root.after(1, lambda : Util.batch_execute_func(Application.enableButton(app.onButton, app.gasChange), \
                                                              app.statusVar.set("OFF"), \
                                                              app.onoff.set("ON"),\
                                                              self.off_pin_seq()))

    def forward(self, app):
        Application.disableButton(app.forward, app.reverse, app.onButton, app.gasChange)
        app.root.after(1, lambda : Util.batch_execute_func(Application.enableButton(app.neutral, app.onButton, app.gasChange), \
                                                              app.statusVar.set("Forward"), \
                                                              self.forward_pin_seq()))
        
    def neutral(self, app):
        Application.disableButton(app.neutral, app.onButton, app.gasChange)
        app.root.after(1, lambda : Util.batch_execute_func(Application.enableButton(app.onButton, app.forward, app.reverse, app.gasChange), \
                                                              app.statusVar.set("Neutral"), \
                                                              self.neutral_pin_seq()))
        
    def reverse(self, app):
        Application.disableButton(app.reverse, app.forward, app.onButton, app.gasChange)
        app.root.after(1, lambda : Util.batch_execute_func(Application.enableButton(app.onButton, app.neutral, app.gasChange), \
                                                              app.statusVar.set("Reverse"), \
                                                              self.reverse_pin_seq()))
        
    def gas(self, app):
        Application.disableButton(app.gasChange, app.onButton)
        app.root.after(1, lambda : Util.batch_execute_func(app.onoff.set('ON'), self.off(app), Application.disableButton(app.gasChange, app.onButton), self.switch_battery(app, True)))

    def on_pin_seq(self):
        self.off_pin_seq()
        time.sleep(1)
        print("Pin KEY")
        GPIO.output(29, GPIO.HIGH)
        time.sleep(1)
        print("Pin ON ENABLE")
        GPIO.output(31, GPIO.HIGH)

    def off_pin_seq(self):
        print('OFF ALL PINS')
        for pin in self.pins:
            GPIO.output(pin, GPIO.LOW)
            time.sleep(self.DEFAULT_PIN_DELAY)

    def neutral_pin_seq(self):
        self.on_pin_seq()

    def forward_pin_seq(self):
        self.neutral_pin_seq()
        time.sleep(1)
        print('Pin FORWARD')
        GPIO.output(37, GPIO.HIGH)

    def reverse_pin_seq(self):
        self.neutral_pin_seq()
        time.sleep(1)
        print('Pin REVERSE')
        GPIO.output(35, GPIO.HIGH)

    def gas_pin_seq(self):
        self.off_pin_seq()
        print('Pin GAS')
        pass

    def switch_battery(self, app, val = None):
        self.bat_one = not self.bat_one if val is None else val
        if self.bat_one:
            print('HIGH')
            time.sleep(1)
            app.lightningVar.set('⚡\n')
            self.charge_pin_seq(True)
        else:
            '''print('LOW')
            serial.arduino_serial.write('a'.encode())
            time.sleep(1)
            app.lightningVar.set('\n⚡')'''
            app.lightningVar.set('\n\n')
            self.charge_pin_seq(False)
        pass

    def charge_pin_seq(self, on=False):
        if on is True:
            GPIO.output(38, GPIO.HIGH)
            GPIO.output(40, GPIO.HIGH)
        else:
            GPIO.output(38, GPIO.LOW)
            GPIO.output(40, GPIO.LOW)

class SpeedometerThread(threading.Thread):

    watchdog_time_since = 0
    
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.app = app
        self.name = "Speedometer"
        self.counter = 0;
        self.speedometer = Speedometer(self, math.pi*25)
        self.speedometer.setup()
        self.event = threading.Event()
        
    def run(self):
        #self.demo()
        try:
            self.speedometerUpdateLoop()
        except:
            pass
        print(self.name + " thread exited gracefully!")

    def demo(self):
       while True:
            if self.counter < 200:
                self.counter += 1
                self.app.speedVar.set(str(self.counter)+"\nmph")
                #time.sleep(1)
            else:
                self.counter = 0

            timeout = 0.1
            if(self.counter > 80):
                timeout = 0.5
            
            if self.app.threadingEvent.wait(timeout=timeout):
                    break

    def speedometerUpdateLoop(self):
        zero_count = 0
        no_zero_count = 0
        zero_timeout = 150
        no_zero_timeout = 150
        while True:
            if time.time() - self.watchdog_time_since > 2:
                self.speedometer.reset()
            speed = self.speedometer.getSpeed()
            self.app.speedVar.set('{0:.0f}'.format(Util.convert_km(speed)) + "\nmi/hr")
            if speed == 0:
                zero_count += 1 if zero_count != zero_timeout else 0
            else:
                no_zero_count += 1 if no_zero_count != no_zero_timeout else 0
            if speed <= 0 and zero_count >= zero_timeout and no_zero_count != 0:
                no_zero_count = 0
                self.app.switchFrameOn(0)
                zero_count = zero_timeout
            elif speed > 0 and no_zero_count >= no_zero_timeout and zero_count != 0:
                zero_count = 0
                self.app.switchFrameOn(1)
                no_zero_count = no_zero_timeout
            if self.event.wait(timeout=1/1000):
               break;
                

    def notifyWatchdog(self):
        self.watchdog_time_since = time.time()

class BatteryVoltageThread(threading.Thread):

    def __init__(self, app):
        threading.Thread.__init__(self)
        self.app = app
        self.name = "BatteryVoltage"
        self.event = threading.Event()

    def run(self):
        self.batteryVoltageUpdateLoop()
        print(self.name + " Exited gracefully!")
        pass

    def batteryVoltageUpdateLoop(self):
        batVar = self.app.batteryInfoVar
        while True:
            batOneVol = 0.00 
            try:
                '''serial.arduino_serial.reset_output_buffer()
                if self.event.wait(timeout=1/2):
                    break'''
                raw = serial.readBatteryInformation().decode('utf-8')
                #print(raw)
                splitted = raw.split(';')
                batOneVol = float(splitted[0])
            except Exception as e:
                print(e)
                #break
            finalString = 'Battery Pack 1\n{0:02d}% {1:02d}V'\
                            .format(int(batOneVol*100/48), int(batOneVol))
            batVar.set(finalString)
            if self.event.wait(timeout=1/1000):
                break
            

class Util:
    
    @staticmethod
    def batch_execute_func(*funcs):
        for f in funcs:
            f

    @staticmethod
    def convert_km(km):
        return km * 0.621

if __name__ == '__main__':
    Application.main()
