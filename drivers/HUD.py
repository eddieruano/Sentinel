# -*- coding: utf-8 -*-
# @Author: Eddie Ruano
# @Date:   2017-06-01 12:03:30
# @Last Modified by:   Eddie Ruano
# @Last Modified time: 2017-06-01 13:11:10

import curses

class HUD(object):
    v_box_ht = 5
    v_box_wt = 30
    def __init__(self):
        self.display = curses.initscr()
        self.leftBox = self.display.subwin(self.v_box_ht, self.v_box_wt, 5, 5)
        self.rightBox = self.display.subwin(self.v_box_ht, self.v_box_wt, 5, 40)
        self.midBox = self.display.subwin(10, 60, 10, 10)
        self.touchBox = self.display.subwin(10, 60, 25, 10)
        self.configureHUD()
    def configureHUD(self):
        curses.noecho()
        self.display.nodelay(True)
        self.display.border(0)
        self.displayHeaderBar()
        # Create Left Window
        self.leftBox.box()
        # Create Right Window
        self.rightBox.box()
        self.leftBox.addstr(1, 5, "Voyager 1 Distance")
        self.rightBox.addstr(1, 5, "Voyager 2 Distance")
        # Create MidSetion Status
        self.midBox.box()
        self.midBox.addstr(1, 21, "Control Status")
        self.midBox.addstr(3, 5, "Voyager Disparity Error +/-: ")
        self.midBox.addstr(4, 5, "ProxV1 Status: ")
        self.midBox.addstr(5, 5, "ProxV2 Status: ")
        self.midBox.addstr(6, 5, "SlowDown Factor: 0x (in Green)")
        self.midBox.addstr(7, 5, "Timeout: 0 (in Green)")
        # Create Touch Box
        self.touchBox.box()
        self.touchBox.addstr(1, 21, "Cap Touch Status")
        self.displayRefresh()
        # Create Serial Box
    def displayHeaderBar(self):
        #Print the Greeting
        self.display.addstr(1, 14, 
            "*******  DESI Mission Control Module v1.0  *******")
        self.display.addstr(2, 14, 
            "**************  Updated April 2017  **************")
        self.displayRefresh()
    def displayRefresh(self):
        self.display.refresh()
        self.leftBox.refresh()
        self.rightBox.refresh()
        self.midBox.refresh()
        self.touchBox.refresh()
    def displayBar (self, iteration):
        total = 30
        prefix = 'StartZone'
        suffix = 'RedZone'
        fill = '█'
        decimals = 1
        length = 35
        # Do work
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        end = "%\r"
        buf = "%s |%s| %s %s %%\n" % (prefix, bar, suffix, percent)
        self.display.addstr(22, 5, buf)
        self.displayRefresh()
    def displayInfo(self, prox1, prox2, status):
        self.updateV1(prox1)
        self.displayRefresh()
    def updateV1(self, distance):
        status = "Green"
        update = str(distance) +  " cm"
        self.display.addstr(8, 8, update)
        if distance < 17.2:
            self.display.addstr(14, 30, "Within Green Zone", curses.A_UNDERLINE)
        elif distance > 17.2 and distance < 30:
            self.display.addstr(14, 30, "Within Yellow Zone", curses.A_UNDERLINE)
            status = "Yellow"
        else:
            self.display.addstr(14, 30, "RED ZONE, Beginning Timeout", curses.A_UNDERLINE)
            status = "Red"
        return status