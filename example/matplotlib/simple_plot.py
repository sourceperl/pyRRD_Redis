#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import matplotlib.pyplot as plt
from pyRRD_Redis import RRD_redis

# init RRD db
rrd = RRD_redis('rrd:test1')

# make up some data
x = []
y = []
for rrv in rrd.get(size=10000):
    x.append(datetime.datetime.fromtimestamp(rrv.timestamp))
    y.append(rrv.value)

# plot
plt.plot(x, y)
plt.gcf().autofmt_xdate()

plt.show()
