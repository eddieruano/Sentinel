#!/usr/bin/python
# @Author: Eddie Ruano
# @Date:   2017-05-01 05:14:54
# @Last Modified by:   Eddie Ruano
# @Last Modified time: 2017-06-03 23:24:13
# 
"""
    MissionControl.py is a debugging tool for DESI_Sentinel
"""
### IMPORT MODULES ###
import sys
import os.path
import signal
import time
# Customs Mods #
import Adafruit_MPR121.MPR121 as MPR121
import RPi.GPIO as GPIO
# Local Modules #
### Set path ###
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import drivers.VoyagerHCSR04 as VoyagerHCSR04
import drivers.DESIConfig as DESIConfig
### Global Variables ###
DESI = DESIConfig.DESI()
Voyager1 = VoyagerHCSR04.Voyager("Voyager1", DESI.PROX1_TRIG, DESI.PROX1_ECHO)
Voyager2 = VoyagerHCSR04.Voyager("Voyager2", DESI.PROX2_TRIG, DESI.PROX2_ECHO)
TouchSense = MPR121.MPR121()

def main():
    # Variables
    proxError = 0.0
    distv1 = 0.0
    distv2 = 0.0
    slack = 0.0
    contact = False
    # Initialize DESI States
    DESI.initDESI()
    # Initialize Voyager Proximity Sensors
    DESI.initProximity(Voyager1, Voyager2)
    if not TouchSense.begin():  # Init TouchSense Capacitive Sensor Array
        print("TSense")
        sys.exit(1)
    try:
        print("Listening")
        GPIO.add_event_detect(DESI.IN_START, GPIO.FALLING, DESI.performStart, DESI.bounceTime)
        GPIO.add_event_detect(DESI.IN_PAUSE, GPIO.FALLING, DESI.performPause, DESI.bounceTime)
        GPIO.add_event_detect(DESI.IN_SPEED0, GPIO.FALLING, DESI.performS0, DESI.bounceTime)
        GPIO.add_event_detect(DESI.IN_SPEED1, GPIO.FALLING, DESI.performS1, DESI.bounceTime)
        GPIO.add_event_detect(DESI.IN_SPEED2, GPIO.FALLING, DESI.performS2, DESI.bounceTime)
        GPIO.add_event_detect(DESI.IN_SPEED3, GPIO.FALLING, DESI.performS3, DESI.bounceTime)
        GPIO.add_event_detect(DESI.IN_SPEED4, GPIO.FALLING, DESI.performS4, DESI.bounceTime)
        #DESI.DESIListen()
        activeFlag = True
        while activeFlag == True:
            activeFlag = True
            command = input("Enter a command: ")
            if command == "start":
                DESI.DESISend("Start")
            elif command == "shutdown":
                DESI.DESISend("Shutdown")
            elif command == "pause":
                DESI.DESISend("Pause")
            elif command == "unpause":
                DESI.DESISend("Pause")
            elif command == "enter":
                DESI.DESISend("Enter")
            elif command == "0":
                DESI.DESISend("Send00")
            elif command == "1":
                DESI.DESISend("Send01")
            elif command == "2":
                DESI.DESISend("Send02")
            elif command == "3":
                DESI.DESISend("Send03")
            elif command == "4":
                DESI.DESISend("Send04")
            elif command == "down":
                DESI.DESISend("SendDown")
            elif command == "alexa":
                DESI.DESISend("SendAlexa")
            else:
                print("Invalid Command")
            print(DESI.State_Main)
            # Query for the proximity of Megan #
            distv1 = Voyager1.get_distance()
            #time.sleep(0.3)
            distv2 = Voyager2.get_distance()
            print(distv1)
            print(distv2)
            #distAverage = (distv1 + distv2) / 2
            #proxError = distv1 - distv2
            #contact = checkContact()
            #state = checkState(distAverage)
            #if state == "Red":
            #    print("Red!")
            #    past_state = state
            #    DESI.send("Pause")
            #    time.sleep(5)
            #    DESI.send(past_state)
            #elif state == "Yellow":
            #    DESI.send("Down")
            #    time.sleep(0.4)
            #    DESI.send("Down")
            #    time.sleep(0.4)
            #    DESI.send("Down")
            #else:
            #    print("Green!")
            #    slack = 30 - distAverage
            #    redux = ((distAverage - 10) / 2) * 10
            #    redux = int(redux)
#           time.sleep(1)
    # Catch Ctrl+C
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Shutdown Mission.")
        #Detector.terminate()
        
### END OF MAIN ###
"""Helper Functions"""
def activateAlexa():
    GPIO.output(DESI.OUT_ALEXA, GPIO.LOW)
    time.sleep(2)
    GPIO.output(DESI.OUT_ALEXA, GPIO.HIGH)
#def signal_handler(signal, frame):
#    global HotwordInterrupt
#    HotwordInterrupt = True
#def interrupt_callback():
#    global HotwordInterrupt
#    return HotwordInterrupt
### MAIN CALL ###
if __name__ == "__main__":
    main()