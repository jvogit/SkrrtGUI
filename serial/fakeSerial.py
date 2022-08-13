import random

class Serial:
   def __init__(self, port, baud):
      print('fakeSerial INIT ' + str(port) + ' ' + str(baud))
   def write(self, data):
      print('fakeSerial write RAW: ' + str(data))
   def reset_output_buffer(self):
      #print('fakeSerial reset_output_buffer')
      pass
   def readline(self):
      return (str(random.randint(0, 48)) + ';' + str(random.randint(0,48)) + ';' + str(random.randint(0,1))).encode()
      
   
