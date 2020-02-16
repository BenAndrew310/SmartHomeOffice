#Running on Rpi

import time
from time import sleep
import threading
import RPi.GPIO as GPIO
import Adafruit_DHT

class FanControl:
    DHT_SENSOR = Adafruit_DHT.DHT22
    DHT_PIN = 4

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    FAN = 12
    GPIO.setup(FAN,GPIO.OUT)
    GPIO.output(FAN,False)
    
    def __init__(self):
        self.temp_threshold=27.0
    
    def run_temperature_monitoring(self):
        while True:
            try:
                humidity,temperature=Adafruit_DHT.read_retry(FanControl.DHT_SENSOR,FanControl.DHT_PIN)
                if humidity is not None and temperature is not None:
                    if float(temperature)>=self.temp_threshold:
                        GPIO.output(FanControl.FAN,True)
                    else:
                        GPIO.output(FanControl.FAN,False)
                else:
                    print("Failed to retrieve temperature and humidity from sensor")
                time.sleep(0.5)
            except KeyboardInterrupt:
                GPIO.cleanup()
                exit()
                
#def main():
 #   run=FanControl()
  #  run.run_temperature_monitoring()
    
#if __name__=="__main__":
 #   main()
