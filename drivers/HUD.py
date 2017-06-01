# -*- coding: utf-8 -*-
# @Author: Eddie Ruano
# @Date:   2017-06-01 12:03:30
# @Last Modified by:   Eddie Ruano
# @Last Modified time: 2017-06-01 12:35:15

import curses

class HUD(object):

    def __init__(self):
        self.display = curses.initscr()
        self.configureHUD()
    def configureHUD(self):
        curses.noecho()
        self.display.nodelay(True)
        self.display.border.(0)
        self.displayHeaderBar()
    def displayHeaderBar(self):
        #Print the Greeting
        self.display.addstr(1, 14, 
            "*******  DESI Mission Control Module v1.0  *******")
        self.display.addstr(2, 14, 
            "**************  Updated April 2017  **************")
        self.displayRefresh()
    def displayRefresh(self):
        self.display.refresh()