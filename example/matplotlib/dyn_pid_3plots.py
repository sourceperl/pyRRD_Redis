#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.animation as animation
from pyRRD_Redis import RRD_redis
import datetime


def rrd2xy(rrd_name, size=600):
    rrd = RRD_redis(rrd_name)
    x = []
    y = []
    for rrv in rrd.get(size=size):
        x.append(datetime.datetime.fromtimestamp(rrv.timestamp))
        y.append(rrv.value)
    return x, y


def animate(i):
    # PID out
    (x, y) = rrd2xy('rrd:pid_out')
    # wipe and redraw
    ax1.clear()
    ax1.set_ylabel('PID out (%)')
    ax1.set_axis_bgcolor('grey')
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    ax1.plot(x, y, 'r', lw=2)
    # # Set point
    (x, y) = rrd2xy('rrd:set_point')
    # # wipe and redraw
    ax2.clear()
    ax2.set_ylabel('SP (bar)')
    ax2.set_axis_bgcolor('grey')
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    ax2.plot(x, y, 'b', lw=2)
    # # Set point
    (x, y) = rrd2xy('rrd:proc_value')
    # wipe and redraw
    ax3.clear()
    ax3.set_ylabel('PV (bar)')
    ax3.set_xlabel('time(s)')
    ax3.set_axis_bgcolor('grey')
    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    #plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45)
    ax3.plot(x, y, 'g', lw=2)

fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1)
fig.canvas.set_window_title('PID test')
ani = animation.FuncAnimation(fig, animate, interval=1000)
fig.autofmt_xdate()
plt.show()
