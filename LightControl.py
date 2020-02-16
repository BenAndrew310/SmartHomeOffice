#Running on Rpi

import time
from time import sleep
import threading
import RPi.GPIO as GPIO

import requests
import json

from TemperatureMonitoring import FanControl

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


TRIG = 16
ECHO = 20
LED  = 18
controlBTN = 22

GPIO.setup(LED,GPIO.OUT)
#GPIO.setup(TRIG,GPIO.OUT)
#GPIO.setup(ECHO,GPIO.IN)
#GPIO.setup(autoBTN,GPIO.IN,pull_up_down=GPIO.PUD_UP)
#GPIO.setup(controlBTN,GPIO.IN)#,pull_up_down=GPIO.PUD_UP)

GPIO.output(LED,False)

ulr = ''
deviceId = "DpvsvmL1"  
deviceKey = "BlKrcqVKHfhSYLSi"

def post_to_mcs(payload): # upload data points to mcs
    host = "http://api.mediatek.com"
    endpoint = "/mcs/v2/devices/" + deviceId + "/datapoints"
    # url = ''.join([host,endpoint])
    url = host + endpoint
    headers = {"Content-type": "application/json", "deviceKey": deviceKey}
    r = requests.post(url,headers=headers,data=json.dumps(payload))
  
def get_from_mcs(id):  # get data points from mcs
    host = "http://api.mediatek.com"
    endpoint = "/mcs/v2/devices/" + deviceId + "/datachannels/" + id + "/datapoints"
    # url = ''.join([host,endpoint])
    url = host + endpoint
    headers = {"Content-type": "application/json", "deviceKey": deviceKey}
    r = requests.get(url,headers=headers)
    value = (r.json()["dataChannels"][0]["dataPoints"][0]["values"]["value"])
    return value

def ComputeDistance(): # compute the distance between any object facing the sensor 
    global TRIG        # and the sensor
    global ECHO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)
    GPIO.output(TRIG, False)
    sleep(0.002)
    GPIO.output(TRIG, True)
    sleep(0.001)
    GPIO.output(TRIG, False)
    
    while GPIO.input(ECHO)==False:
        a=0
    time1= time.time()
    while GPIO.input(ECHO)==True:
        a=1
    time2= time.time()
    
    during=time2-time1
    
    return during*340/2 *100

def set_led(control): # depending on the control value, sets the LED on or off and
    global LED        # updates the LED's state on the cloud
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED,GPIO.OUT)
    if control==1:
        GPIO.output(LED,True)
        payload={"datapoints":[{"dataChnId":"1","values":{"value":1}}]}
    else:
        GPIO.output(LED,False)
        payload={"datapoints":[{"dataChnId":"1","values":{"value":0}}]}
    post_to_mcs(payload) # update the LED's state

def toggleLED(control): # when the button is pressed, change the control value on the cloud
    if control==1:      # consequently toggling the LED
        payload={"datapoints":[{"dataChnId":"2","values":{"value":0}}]}
    else:
        payload={"datapoints":[{"dataChnId":"2","values":{"value":1}}]}
    post_to_mcs(payload)
    
def turn_led_on(delay): # turns the LED on for a certain delay specified in the cloud
    global LED          # then turns it off while updating its state in the cloud
    GPIO.output(LED,True)
    payload={"datapoints":[{"dataChnId":"1","values":{"value":1}}]}
    post_to_mcs(payload)
    sleep(delay*60)
    GPIO.output(LED,False)
    payload={"datapoints":[{"dataChnId":"1","values":{"value":0}}]}
    post_to_mcs(payload)
    
def display_feedback(mode,control,delay):
    print("LED on mode",mode,end="\t")
    print("Control set to",control,end="\t")
    print("Delay set to",delay)
    
def check_controlBTN(): # check if the button has been pressed 
    print("Thread has started")
    global controlBTN
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(controlBTN,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    while True:
        try:
            control=int(get_from_mcs("2"))
            if GPIO.input(controlBTN)==False:
                toggleLED(control)
                sleep(0.2)
            sleep(1)
        except KeyboardInterrupt:
            GPIO.cleanup()
            exit()
    

def main():
    ########## few initializations before the loop begins ############################
    LEDonDelay=1
    distanceThreshold=20
    post_to_mcs({"datapoints":[{"dataChnId":"4","values":{"value":LEDonDelay}}]})
    post_to_mcs({"datapoints":[{"dataChnId":"1","values":{"value":0}}]})
    ########## Start a new thread to check if the button has been pressed ############
    t=threading.Thread(target=check_controlBTN)
    t.start()
    f=FanControl() # create a FanControl object
    t2=threading.Thread(target=f.run_temperature_monitoring)
    t2.start()
    while True:
        try:
            mode=int(get_from_mcs('3'))
            control=int(get_from_mcs('2'))
            delay=int(get_from_mcs('4'))
            display_feedback(mode,control,delay)
            
            if mode==1:
                dist=ComputeDistance()
                if dist<=distanceThreshold:
                    try:
                        turn_led_on(delay)
                    except:
                        print("There's been an error.\nDelay is set to default")
                        turn_led_on(1)
                    sleep(0.2)
                else:
                    GPIO.output(LED,False)
                    sleep(0.2)
            else:
                set_led(control)

                
            sleep(5)
        except KeyboardInterrupt:
            GPIO.cleanup()
            exit()
    
if __name__=="__main__":
    main()
