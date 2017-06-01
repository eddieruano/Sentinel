# -*- coding: utf-8 -*-
# @Author: Eddie Ruano
# @Date:   2017-06-01 07:23:39
# @Last Modified by:   Eddie Ruano
# @Last Modified time: 2017-06-01 07:29:45

import RPi.GPIO as GPIO

def initProximity(sensorV1, sensorV2):
    # Set up the correct In/Out Scheme for send/receive
    GPIO.setup(sensorV1.trigger_pin, GPIO.OUT)
    GPIO.setup(sensorV1.echo_pin, GPIO.IN)
    GPIO.setup(sensorV2.trigger_pin, GPIO.OUT)
    GPIO.setup(sensorV2.echo_pin, GPIO.IN)
