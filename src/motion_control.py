# -*- coding=utf-8 -*-
# motion_control.py

"""
Based on the location of target in current image, control the motor to move towards the target.
"""

from gpiozero import Motor
from time import sleep
import cv2
import numpy as np
import imutils

cv2.VideoCapture(0)