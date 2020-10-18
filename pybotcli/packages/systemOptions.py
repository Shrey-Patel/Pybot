# -*- coding: utf-8 -*-
import os
import subprocess

from utilities.GeneralUtilities import IS_MACOS


def turn_off_screen():
    if IS_MACOS:
        os.system('pmset displaysleepnow')
    else:
        os.system('xset dpms force off')



