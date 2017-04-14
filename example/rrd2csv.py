#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pyRRD_Redis import RRD_redis, StepAddFunc

# some const
TAG_NAME = 'test1'

# init RRD db
rrd = RRD_redis('rrd:' + TAG_NAME, size=2048, step=1.0, add_func=StepAddFunc.last)
# dump database
for rrv in rrd.get():
    print(rrv.time_str+';'+rrv.value_str)
