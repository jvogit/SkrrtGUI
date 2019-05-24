import serial
import time
import random
try:
    arduino_serial = serial.Serial('/dev/ttyUSB0', 9600)
    print('Arduino Port Open USB 0')
except:
    try:
        arduino_serial = serial.Serial('/dev/ttyUSB1', 9600)
        print('Arduino Port Open USB 1')
    except:
        arduino_serial = None
        print('Arduino Port Not Detected USB0 or USB1')
        
def readBatteryInformation():
    global arduino_serial
    try:
        if(arduino_serial is None):
            return 'error'.encode()
        return arduino_serial.readline()
    except Exception as e:
        print(e)
        return 'error'.encode()

