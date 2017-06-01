# -*- coding: utf-8 -*-
# @Author: Eddie Ruano
# @Date:   2017-06-01 12:03:30
# @Last Modified by:   Eddie Ruano
# @Last Modified time: 2017-06-01 12:38:54

import curses

class HUD(object):
    v_box_ht = 5
    v_box_wt = 30
    def __init__(self):
        self.display = curses.initscr()
        self.configureHUD()
    def configureHUD(self):
        curses.noecho()
        self.display.nodelay(True)
        self.display.border(0)
        self.displayHeaderBar()
        self.leftBox = self.display.subwin(self.v_box_ht, self.v_box_wt, 5, 5)
    def displayHeaderBar(self):
        #Print the Greeting
        self.display.addstr(1, 14, 
            "*******  DESI Mission Control Module v1.0  *******")
        self.display.addstr(2, 14, 
            "**************  Updated April 2017  **************")
        self.displayRefresh()
    def displayRefresh(self):
        self.display.refresh()