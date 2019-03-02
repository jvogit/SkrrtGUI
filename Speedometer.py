from RPi import GPIO as GPIO
import time
class Speedometer:

    pin = 0
    circumference = 0
    start_time = 0
    speed = 0
    
    def __init__(self, watchdogThread, circumference, pin=18):
        self.pin = pin
        self.watchdogThread = watchdogThread
        self.circumference = circumference

    def setup(self):
        GPIO.setup(self.pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback = self.calc_speed, bouncetime=20)
        
    def calc_speed(self, val):
        self.watchdogThread.notifyWatchdog()
        if(self.start_time == 0):
            self.start_time = time.time()
            return None
        elapse = time.time() - self.start_time
        rpm = 1/elapse * 60
        dist_km = self.circumference/100000
        km_per_sec = dist_km / elapse
        km_per_hour = km_per_sec * 3600
        self.speed = km_per_hour
        self.start_time = time.time()

    def getSpeed(self):
        return self.speed

    def reset(self):
        self.start_time = 0
        self.speed = 0
