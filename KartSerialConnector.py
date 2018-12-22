import serial
import time
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
            return '0.00;0.00'.encode()
        arduino_serial.flushOutput()
        
        return arduino_serial.readline()
    except:
        print('Cannot read Serial readline')
        return '0.00;0.00'.encode()

