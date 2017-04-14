#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.animation as animation
from pyRRD_Redis import RRD_redis
import argparse
import datetime


def rrd2xy(rrd_name, size):
    rrd = RRD_redis(rrd_name)
    x = []
    y = []
    for rrv in rrd.get(size=size):
        x.append(datetime.datetime.fromtimestamp(rrv.timestamp))
        y.append(rrv.value)
    return x, y


def animate(i):
    # PID out
    (x, y) = rrd2xy('rrd:' + args.tag_name, size=args.number)
    # wipe and redraw
    ax1.clear()
    if args.unit:
        ax1.set_ylabel(args.tag_name + ' (' + args.unit + ')')
    else:
        ax1.set_ylabel(args.tag_name)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax1.plot(x, y, 'r', lw=2)

# parse args
parser = argparse.ArgumentParser()
parser.add_argument('tag_name', type=str, help='tag name like L1_M_WOBBE')
parser.add_argument('-u', '--unit', type=str, help='unit like \'wh/nm3\'')
parser.add_argument('-n', '--number', type=int, help='number of RRD samples from now', default=360)
args = parser.parse_args()
# configure plot
fig, (ax1) = plt.subplots(nrows=1, ncols=1)
fig.canvas.set_window_title(args.tag_name)
ani = animation.FuncAnimation(fig, animate, interval=1000)
fig.autofmt_xdate()
plt.show()
