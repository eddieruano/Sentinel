#!/usr/bin/python
# @Author: Eddie Ruano
# @Date:   2017-05-01 05:14:54
# @Last Modified by:   Eddie Ruano
# @Last Modified time: 2017-06-04 04:08:45
# 
"""
    MissionControl.py is a debugging tool for DESI_Sentinel
"""
### IMPORT MODULES ###
import sys
import os.path
import signal
import collections
import pyaudio
import wave
import time
from math import floor
# Customs Mods #
import Adafruit_MPR121.MPR121 as MPR121
import RPi.GPIO as GPIO
# Local Modules #
### Set path ###
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import drivers.VoyagerHCSR04 as VoyagerHCSR04
import drivers.DESIConfig as DESIConfig
TOP_DIR = os.path.dirname(os.path.abspath(__file__))
DING = os.path.join(TOP_DIR, "resources/ding.wav")
### Global Variables ###
DESI = DESIConfig.DESI()
Voyager1 = VoyagerHCSR04.Voyager("Voyager1", DESI.PROX1_TRIG, DESI.PROX1_ECHO)
Voyager2 = VoyagerHCSR04.Voyager("Voyager2", DESI.PROX2_TRIG, DESI.PROX2_ECHO)
TouchSense = MPR121.MPR121()
CONST_REDUX = 0.1
CONST_ZONE_FIX = 0.0
Proximity = 0
FlagDisparity = False

def main():
    global FlagDisparity
    global Proximity
    # Variables
    contact = False
    dFlag = True
    lastZone = -1.0
    subZone = 0.0
    redFlag = False
    saveSpeed = DESI.State_Speed
    # Initialize DESI States
    DESI.initDESI()
    # Initialize Voyager Proximity Sensors
    DESI.initProximity(Voyager1, Voyager2)
    if not TouchSense.begin():  # Init TouchSense Capacitive Sensor Array
        print("TSense")
        sys.exit(1)
    GPIO.add_event_detect(DESI.IN_START, GPIO.FALLING)
    GPIO.add_event_detect(DESI.IN_PAUSE, GPIO.FALLING)
    GPIO.add_event_detect(DESI.IN_SPEED0, GPIO.FALLING)
    GPIO.add_event_detect(DESI.IN_SPEED1, GPIO.FALLING)
    GPIO.add_event_detect(DESI.IN_SPEED2, GPIO.FALLING)
    GPIO.add_event_detect(DESI.IN_SPEED3, GPIO.FALLING)
    GPIO.add_event_detect(DESI.IN_SPEED4, GPIO.FALLING)
    try:
        print("Listening")
        #DESI.DESIListen()
        activeFlag = True
        while activeFlag == True:
            i = 0
            if(GPIO.event_detected(DESI.IN_START)):
                print("start")
                DESI.DESISend("Start")
            elif(GPIO.event_detected(DESI.IN_PAUSE)):
                print("pause")
                DESI.DESISend("Pause")
            elif(GPIO.event_detected(DESI.IN_SPEED0)):
                print("0")
                DESI.DESISend("Send00")
            elif(GPIO.event_detected(DESI.IN_SPEED1)):
                print("1")
                DESI.DESISend("Send01")
            elif(GPIO.event_detected(DESI.IN_SPEED2)):
                print("2")
                DESI.DESISend("Send02")
            elif(GPIO.event_detected(DESI.IN_SPEED3)):
                print("3")
                DESI.DESISend("Send03")
            elif(GPIO.event_detected(DESI.IN_SPEED4)):
                print("4")
                DESI.DESISend("Send04")
            else:
                pass

            Proximity = queryDistance()
            if FlagDisparity:
                FlagDisparity = False;
            print(Proximity)
            subZone = floor(Proximity - DESI.Zone_Yellow) + 1.0
            if Proximity == -1.0:
                print ("Error")
            elif(Proximity > DESI.Zone_Yellow and subZone != lastZone):
                subRedux = DESI.State_Speed * CONST_REDUX * 10
                redux = subZone * subRedux
                print(subRedux)
                print(subZone)
                print(redux)
                while i < redux:
                    DESI.DESISend("SendDown")
                    i+=1
                lastZone = subZone
                print("refresh")
            elif Proximity > DESI.Zone_Red and not redFlag:
                saveSpeed = DESI.State_Speed
                DESI.DESISend("Send00")
                print(ave)
                redFlag = True
            elif Proximity < DESI.Zone_Red and redFlag:
                DESI.DESISend("Send01")
                redFlag = False
            else:
                pass
            time.sleep(0.05)
            # Query for the proximity of Megan #
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
def play_audio_file(fname=DING):
    """Plays audio
    :param str fname: wave file name
    :return: None
    """
    ding_wav = wave.open(fname, 'rb')
    ding_data = ding_wav.readframes(ding_wav.getnframes())
    audio = pyaudio.PyAudio()
    stream_out = audio.open(
        format=audio.get_format_from_width(ding_wav.getsampwidth()),
        channels=ding_wav.getnchannels(),
        rate=ding_wav.getframerate(), input=False, output=True)
    stream_out.start_stream()
    stream_out.write(ding_data)
    time.sleep(0.2)
    stream_out.stop_stream()
    stream_out.close()
    audio.terminate()
def queryDistance():
    global FlagDisparity
    global Proximity
    error = False
    distv1 = Voyager1.get_distance()
    distv2 = Voyager2.get_distance()
    # Sanitize
    distv1 = distv1 - 3.5
    distv2 = distv2 - 3.5
    if distv1 < 0 or distv1 > 15:
        distv1 = distv2
        error = True
    if distv2 < 0 or distv2 > 15 and not error:
        distv2 = distv1
    if error:
        ave = -1.0
    #print(distv1)
    #print(distv2)
    ave = floor((distv1 + distv2) / 2)
    if (abs(ave - Proximity) > 4) and not FlagDisparity:
        ave = Proximity
        FlagDisparity = True
    else:
        FlagDisparity == False
    #    return Distance
    return ave
#def signal_handler(signal, frame):
#    global HotwordInterrupt
#    HotwordInterrupt = True
#def interrupt_callback():
#    global HotwordInterrupt
#    return HotwordInterrupt
### MAIN CALL ###
if __name__ == "__main__":
    main()