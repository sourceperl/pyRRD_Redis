#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import matplotlib.pyplot as plt
from pyRRD_Redis import RRD_redis

# init RRD db
data1 = RRD_redis('rrd:test1')

# make up some data
x = [datetime.datetime.fromtimestamp(rrv.timestamp) for rrv in data1.get()]
y = [rrv.value for rrv in data1.get()]

# plot
plt.plot(x, y)
plt.gcf().autofmt_xdate()

plt.show()
