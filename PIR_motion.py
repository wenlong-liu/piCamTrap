"""
This is the part of piCamTrap, copyright @ Wenlong Liu.
Created on July 15,2017

This script will initialize a PIR sensor to detection motions.
Platform: Raspberry Pi 3 Model B.
"""
import time
import logging
import RPi.GPIO as GPIO


def _logging(*args):
    print("{} at {}".format(args,time.strftime("%Y-%M-%D %H:%M:%S")))


def run(mpin, interval = 0.5):
    """
    The function will run. if Triggered, it iwll logging and return a stat.
    :param mpin: The pin to connect PIR sensor.
    :param interval: The forced interval for PIR sensor
    :return: Trigger, True or false.
    """
    # Set up sensor mode.
    GPIO.setmode(GPIO.BCM)
    # True = detected, False = not triggered.
    trigger = GPIO.setup(mpin, GPIO.IN)

    if trigger:
        _logging("Motion detected")

    return trigger
