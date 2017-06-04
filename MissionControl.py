#!/usr/bin/python
# @Author: Eddie Ruano
# @Date:   2017-05-01 05:14:54
# @Last Modified by:   Eddie Ruano
# @Last Modified time: 2017-06-04 01:14:07
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



def main():
    # Variables
    proxError = 0.0
    distv1 = 0.0
    distv2 = 0.0
    slack = 0.0
    contact = False
    ave = 0.0
    i = 0
    dFlag = True
    # Initialize DESI States
    DESI.initDESI()
    # Initialize Voyager Proximity Sensors
    DESI.initProximity(Voyager1, Voyager2)
    if not TouchSense.begin():  # Init TouchSense Capacitive Sensor Array
        print("TSense")
        sys.exit(1)
    try:
        print("Listening")
        GPIO.add_event_detect(DESI.IN_START, GPIO.FALLING, DESI.performStart, DESI.Time_Bounce)
        GPIO.add_event_detect(DESI.IN_PAUSE, GPIO.FALLING, DESI.performPause, DESI.Time_Bounce)
        GPIO.add_event_detect(DESI.IN_SPEED0, GPIO.FALLING, DESI.performS0, DESI.Time_Bounce)
        GPIO.add_event_detect(DESI.IN_SPEED1, GPIO.FALLING, DESI.performS1, DESI.Time_Bounce)
        GPIO.add_event_detect(DESI.IN_SPEED2, GPIO.FALLING, DESI.performS2, DESI.Time_Bounce)
        GPIO.add_event_detect(DESI.IN_SPEED3, GPIO.FALLING, DESI.performS3, DESI.Time_Bounce)
        GPIO.add_event_detect(DESI.IN_SPEED4, GPIO.FALLING, DESI.performS4, DESI.Time_Bounce)
        #DESI.DESIListen()
        activeFlag = True
        lastZone = 0.0
        while activeFlag == True:
            i = 0
            ave = queryDistance()
            subRedux = DESI.State_Speed * CONST_REDUX * 10
            subZone = floor(ave - DESI.Zone_Yellow) + 1.0
            redux = subZone * subRedux
            print(subRedux)
            print(subZone)
            print(redux)
            print(ave)
            if (ave > DESI.Zone_Yellow) and (lastZone != subZone):
                lastZone = subZone
                while i < redux:
                    DESI.DESISend("SendDown")
                    i+=1
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
    distv1 = Voyager1.get_distance()
    distv2 = Voyager2.get_distance()
    # Sanitize
    distv1 = distv1 - 3.5
    distv2 = distv2 - 3.5
    print(distv1)
    print(distv2)
    ave = (distv1 + distv2) / 2
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