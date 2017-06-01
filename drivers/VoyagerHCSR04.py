#!/usr/bin/python
# @Author: Eddie Ruano
# @Date:   2017-05-01 05:14:54
# @Last Modified by:   Eddie Ruano
# @Last Modified time: 2017-06-01 14:51:11

"""
    DESI uses two HCSR04 proximity sensors to determine Megan's postition on the treadmill.
"""
# Libraries
import RPi.GPIO as GPIO
import time
 
class Voyager:
    
    Timeout = time.ctime(1)

    """ Begin VoyagerHCSR04 class structure """
    def __init__(self, name, t_pin, e_pin):
        self.name = name
        self.trigger_pin = t_pin
        self.echo_pin = e_pin
        self.status = "Pass"

    def update_status(self, stat):
        self.status = stat
        return self.status

    def self_check(self):
        if self.get_distance() != -1:
            self.status = "Pass"
            return True
        else:
            self.status = "Fail"
            return False
    def get_distance(self):
        # Set Trigger to HIGH
        GPIO.output(self.trigger_pin, True)
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.trigger_pin, False)

        # Create holders for times
        StopWatch = time.time()
        StartTime = time.time()

        StopTime = time.time()
 
        # save StartTime
        while GPIO.input(self.echo_pin) == 0:
            StartTime = time.time()
            if StopWatch > Timeout:
                return -1
            else
                StopWatch += StartTime
 
        # save time of arrival
        while GPIO.input(self.echo_pin) == 1:
            StopTime = time.time()
 
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
        return distance
