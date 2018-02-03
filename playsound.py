# -*- coding:utf-8 -*-
import time
import sys
import os

def soundStart():
    if sys.platform.find('linux') != -1 or sys.platform.find('darwin') != -1:
        os.system("afplay train.mp3")
        os.system("afplay train.mp3")
        os.system("afplay train.mp3")
    else:
        os.system("mplayer.exe train.mp3")
        os.system("mplayer.exe train.mp3")
        os.system("mplayer.exe train.mp3")

soundStart()