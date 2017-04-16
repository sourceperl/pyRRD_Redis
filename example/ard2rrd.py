#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Arduino UNO A0 value to RRD db
#  - read an integer from a serial port and store it on RRD redis database

import serial
from pyRRD_Redis import RRD_redis, StepAddFunc

# some const
TAG_NAME = 'arduino_a0'

# init serial port and RRD db
ser = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=1)
rrd = RRD_redis('rrd:' + TAG_NAME, size=2048, step=1.0, add_func=StepAddFunc.avg)
# fill database
while True:
    # read A0 on serial
    try:
        a0 = int(ser.readline())
        if not 0 <= a0 <= 1023:
            raise ValueError
    except ValueError:
        a0 = None
    # store value
    if a0 is not None:
        # store with scale to 0/100 %
        rrd.add_step(float(a0) * 100 / 1023)
