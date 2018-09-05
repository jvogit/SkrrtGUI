try:
    from tkinter import Text,Frame,Tk,Button,Label,Entry
    from tkinter.constants import NORMAL,DISABLED,END
except ImportError:
    from Tkinter import Text,Frame,Tk,Button,Label,Entry
    from Tkinter.constants import NORMAL,DISABLED,END
import RPi.GPIO as GPIO
import time

"""
gpio pins 36-40 even, 29-37 odd
29 - power/keyswitch
31 - enable
33 - gas (unused)
35 - reverse
37 - forward
40 - hall
"""
class CartGUI:
    def __init__(self, window):
        self.window = window
        self.window.geometry("600x400")
        self.window.resizable(width=False, height=False)
        self.window.title("RED HYBRID SUPER CAR")
        
        global pins
        pins = (29,31,35,37)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(pins, GPIO.OUT)
        GPIO.setup(hall, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.add_event_detect(hall,GPIO.FALLING,callback=get_pulse)
        
        frame = Frame(self.window, height=220, width=600, bg="#d1d1d1")
        frame.grid(row=1, column=0, sticky="NW")
        frame.grid_propagate(0)
        infoFrame = Frame(self.window, bg="#f5f5f5", height=180, width=600)
        infoFrame.grid(row=0, column=0)
        infoFrame.grid_propagate(0)
        
        self.textLabel = Label(infoFrame, text="Status", font=("Courier", 16, "bold"), width=6)
        self.textLabel.grid(row=0, column=0, padx=(20,0), pady=(20,0))
        
        self.text = Text(infoFrame, state=NORMAL, font=('Courier', 15),
                            height=1, width=35)
        self.text.insert(1.0, 'RED HYBRID by Class of 2018')
        self.text.config(state=DISABLED)
        self.text.grid(row=0, column=1, columnspan=3, padx=20, pady=(10,0))
        
        self.batteryLabel = Label(infoFrame, text="Battery\nLevel", font=("Courier", 16, "bold"))
        self.batteryLabel.grid(row=1, column=0, padx=(20,0), pady=(10,0))
        
        self.batteryLevel = Entry(infoFrame, state=NORMAL, font=('Courier', 32), width=4)
        self.batteryLevel.grid(row=1, column=1, padx=(20,0), pady=(10,0), sticky="NW")
        self.batteryLevel.insert(0, "WIP")
        self.batteryLevel.config(state=DISABLED)
        
        self.currentPowerLabel = Label(infoFrame, text="Power\nsource", font=("Courier", 16, "bold"))
        self.currentPowerLabel.grid(row=2, column=0, padx=(20,0), pady=(10,0))
        
        self.currentPower = Entry(infoFrame, state=DISABLED, font=('Courier', 32), width=12)
        self.currentPower.grid(row=2, column=1, columnspan=3, padx=(20,0), pady=(10,0), sticky="NW")
        
        self.speedLabel = Label(infoFrame, text="Speed\nkm/h", font=("Courier", 16, "bold"))
        self.speedLabel.grid(row=1, column=2, pady=(10,0))
        
        self.speed = Entry(infoFrame, state=DISABLED, font=('Courier', 32), width=5)
        self.speed.grid(row=1, column=3, padx=(20,0), pady=(10,0), sticky="NW")
        
        self.off = Button(frame, state=DISABLED, bg="silver",
                            text="OFF", font=('Courier', 16),
                            height=3, width=8, command=self.off_car)
        self.off.grid(row=1, column=0, padx=(100,10), pady=10)
        
        self.start = Button(frame,
                            text="START/\nNEUTRAL", bg="white", font=('Courier', 16),
                            height=3, width=8, command=self.start_car)                          
        self.start.grid(row=0, column=0, padx=(100,10), pady=(10,10))
        
        self.reverse = Button(frame, state=DISABLED, bg="silver",
                            text="Reverse", font=('Courier', 16),
                            height=3, width=8, command=self.reverse_car)
        self.reverse.grid(row=1, column=1, padx=10, pady=10)
        
        self.forward = Button(frame, state=DISABLED, bg="silver",
                            text="Forward", font=('Courier', 16),
                            height=3, width=8, command=self.forward_car)        
        self.forward.grid(row=0, column=1, padx=10, pady=(10,10))
        
        self.gas = Button(frame, state=DISABLED, bg="silver",
                            text="WIP", font=('Courier', 19),
                            height=6, width=7)
        self.gas.grid(row=0, rowspan=2, column=2, padx=10, pady=(9,10))
        
    def start_car(self):
        self.off_car()
        self.text.config(state=NORMAL)
        self.text.delete(1.0, END)
        self.text.insert(1.0, 'Go kart on!')
        self.text.config(state=DISABLED)
        self.start.config(state=DISABLED, bg="silver")
        self.currentPower.config(state=NORMAL)
        self.speed.config(state=NORMAL)
        self.forward.config(state=NORMAL, bg="white", fg="black")
        self.reverse.config(state=NORMAL, bg="white", fg="black")
        self.gas.config(state=NORMAL, bg="white", fg="black")
        self.off.config(state=NORMAL, bg="white", fg="black")
        GPIO.output(29, GPIO.HIGH)
        time.sleep(1.5)
        GPIO.output(31, GPIO.HIGH)
        self.speed_output()

    def off_car(self):
        global pins
        for i in pins:  
            GPIO.output(i, GPIO.LOW)
            time.sleep(0.05)
        self.text.config(state=NORMAL)
        self.text.delete(1.0, END)
        self.text.insert(1.0, 'Go kart off.')
        self.text.config(state=DISABLED)
        self.off.config(state=DISABLED, bg="silver")
        self.start.config(state=NORMAL, bg="white", fg="black")
        self.forward.config(state=DISABLED, bg="silver")
        self.reverse.config(state=DISABLED, bg="silver")
        self.speed_output()

    def forward_car(self):
        self.start_car()
        GPIO.output(37, GPIO.HIGH)
        self.text.config(state=NORMAL)
        self.text.delete(1.0, END)
        self.text.insert(1.0, 'FORWARD')
        self.text.config(state=DISABLED)
        self.gas.config(state=DISABLED, bg="silver")
        self.forward.config(state=DISABLED, bg="silver")
        self.reverse.config(state=DISABLED, bg="silver")
        self.start.config(state=NORMAL, bg="white", fg="black")
        self.speed_output()

    def reverse_car(self):
        self.start_car()
        GPIO.output(35, GPIO.HIGH)
        self.text.config(state=NORMAL)
        self.text.delete(1.0, END)
        self.text.insert(1.0, 'REVERSE')
        self.text.config(state=DISABLED)
        self.gas.config(state=DISABLED, bg="silver")
        self.forward.config(state=DISABLED, bg="silver")
        self.reverse.config(state=DISABLED, bg="silver")
        self.start.config(state=NORMAL, bg="white", fg="black")
        self.speed_output()

    def gas(self):
        self.off_car()
        GPIO.output(33, GPIO.HIGH)
        self.gas.config(state=DISABLED, bg="silver")
        self.text.config(state=NORMAL)
        self.text.delete(1.0, END)
        self.text.insert(1.0, 'Using gas motor.')
        self.text.config(state=DISABLED)

    def electric(self):
        GPIO.output(33, GPIO.LOW)
        time.sleep(0.5)
        GPIO.output(29, GPIO.HIGH)
        time.sleep(1.5)
        GPIO.output(31, GPIO.HIGH)
        self.text.config(state=NORMAL)
        self.text.delete(1.0, END)
        self.text.insert(1.0, 'Using electric motor.')
        self.text.config(state=DISABLED)
        self.start.config(state=NORMAL, bg="white", fg="black")
        self.forward.config(state=NORMAL, bg="white", fg="black")
        self.reverse.config(state=NORMAL, bg="white", fg="black")
        self.gas.config(state=NORMAL, bg="white", fg="black")
        
    def speed_output(self):
        if GPIO.input(35) ^ GPIO.input(37):
            self.speed.config(state=NORMAL)
            self.speed.delete(0, END)
            self.speed.insert(0, get_speed())
            self.speed.after(200, self.speed_output)
        else:
            self.speed.delete(0, END)
            self.speed.insert(0, "OFF")
            self.speed.after(200, self.speed_output)

pulse = 0
distance = 0
rpm = 0.00
speed = 0.00
wheel_c = 10.3 * 2.54*3.14/100
multiplier = 0
hall = 40
elapse = 0.00
addme = 0
start = time.time()

def get_pulse(n):
    global elapse,distance,start,pulse,speed,rpm,multiplier
    cycle = 0
    pulse+=1
    cycle+=1
    if pulse > 0:
        elapse = time.time() - start
        pulse -=1
    if cycle > 0:
        distance += wheel_c
        cycle -= 1

    multiplier = 3600/elapse
    speed = (wheel_c*multiplier)/1000
    rpm = 1/elapse *60

    start = time.time()

def get_speed():
    return speed

def clean():
    GPIO.cleanup()
    root.destroy()

if __name__ == "__main__":
    root = Tk()
    gui = CartGUI(root)
    root.protocol("WM_DELETE_WINDOW", clean)
    root.mainloop()

    
