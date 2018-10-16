import serial

arduino_serial = serial.Serial('COM4', 9600)

def readBatteryInformation():
    global arduino_serial
    try:
        return arduino_serial.readline()
    except:
        print('Arduino port error. Is plugged in? Is port busy? Restart required.')
        return '0;0;0'

