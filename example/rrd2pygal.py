#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygal
from pyRRD_Redis import RRD_redis

# init RRD db
data1 = RRD_redis('rrd:test1')
# build a SVG graph
line_chart = pygal.Line()
line_chart.title = 'Data evolution (RAW value)'
x = []
l1 = []
for rrv in data1.get(size=100):
    x.append(rrv.time_str)
    l1.append(rrv.value)
x.reverse()
l1.reverse()
line_chart.x_labels = x
line_chart.add('raw', l1)
line_chart.render_to_file('/tmp/my_rrd_sample_chart.svg')
