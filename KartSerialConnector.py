import serial
try:
    arduino_serial = serial.Serial('/dev/ttyUSB0', 9600)
    print('success i can see arduino usb port?')
except:
    arduino_serial = None
    print('Oh no! The Arduino could not be detected. Check proper COM port')
def readBatteryInformation():
    global arduino_serial
    try:
        return arduino_serial.readline()
    except:
        print('Arduino port error. Is plugged in? Is port busy? Restart required.')
        return '0;0;0'

