import threading
import time
BOARD = "Board"
OUT = "Out"
IN = "In"
LOW = "LOW"
HIGH = "HIGH"
PUD_UP = "PUD_UP"
FALLING = "FALLING"

def setmode(a):
   print(str(a))
def setup(a, b, pull_up_down = ''):
   print("Call GPIO setup " + str(a) + " " + str(b) + " " + pull_up_down) 
def output(a, b):
   print("Call GPIO output " + str(a) + " " + str(b))
def cleanup():
   print("Call GPIO clean up")
def setmode(a):
   print("Call GPIO setmode " + str(a))
def setwarnings(flag):
   print("Call GPIO setwarnings " + str(flag))
def add_event_detect(a, b, callback, bouncetime):
   print("Call GPIO add_event_detect " + str(a) + " " + str(b))
   threading.Thread(target=lambda : speedo_mock(callback)).start()
def input(a):
   print("Call GPIO input " + str(a))
def speedo_mock(callback):
   count = 0
   while True:
      if count == 10:
         break
      count += 1
      callback(1)
      time.sleep(1)
   
