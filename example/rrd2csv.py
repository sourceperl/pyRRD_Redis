#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import time
from pyRRD_Redis import RRD_redis, StepAddFunc

# init RRD db
rrd = RRD_redis('rrd:test1', size=2048, step=1.0, add_func=StepAddFunc.last)
# dump database
for rrv in rrd.get_rrd_val():
    print(rrv.time_str+';'+rrv.value_str)
