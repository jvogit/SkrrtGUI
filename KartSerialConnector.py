import serial

arduino_serial = serial.Serial('COM4', 9600)

def readBatteryInformation():
    global arduino_serial
    return arduino_serial.readline()

