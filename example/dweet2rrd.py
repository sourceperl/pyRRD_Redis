#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from pyRRD_Redis import RRD_redis, StepAddFunc
import json
import socket
import urllib.parse
import urllib.request
import urllib.error


# some class
class Dweet(object):
    HEADS = {'Content-type': 'application/json'}
    UPDATE_URL = 'https://dweet.io/dweet/for/'
    GET_URL = 'https://dweet.io/get/latest/dweet/for/'

    def __init__(self, dweet_id):
        self.dweet_id = str(dweet_id)
        # set timeout to 10 seconds (default is none)
        socket.setdefaulttimeout(10)

    def update(self, fields):
        # do update request
        try:
            request = urllib.request.Request(Dweet.UPDATE_URL + self.dweet_id, headers=Dweet.HEADS,
                                             data=json.dumps(fields).encode('utf-8'))
            urllib.request.urlopen(request)
            return True
        except urllib.error:
            return False

    def get(self):
        # do get request
        try:
            request = urllib.request.Request(Dweet.GET_URL + self.dweet_id, headers=Dweet.HEADS)
            response = urllib.request.urlopen(request)
            data = response.read().decode('utf-8')
            return json.loads(data)
        except urllib.error:
            return None

# init
rrds = {}
dw = Dweet(dweet_id='0d328b86-fcba-469e-a31a-adfad51be68a')

# main loop
while True:
    try:
        # get dweet json msg as dict
        d = dw.get()['with'][0]['content']
        # setRRD for all dweet floats vars
        for var_name in d:
            rrds[var_name] = rrds.get(var_name, RRD_redis(var_name, size=8640, step=10.0))
            try:
                rrds[var_name].add_step(float(d[var_name]))
            except ValueError:
                pass
    except (IndexError, TypeError, KeyError):
        pass
    # wait for next loop
    time.sleep(10.0)
