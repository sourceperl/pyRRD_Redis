#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import time
from pyRRD_Redis import RRD_redis, StepAddFunc

# some const
TAG_NAME = 'test1'

# init RRD db
rrd = RRD_redis('rrd:' + TAG_NAME, size=2048, step=1.0, add_func=StepAddFunc.avg)
# fill database (8000 samples with 1ms between us, step set to 1s)
# "step=1.0, add_func=StepAddFunc.avg" can be helpful if sample source is noisy
for i in range(0, 8000):
    rrd.add_step(10 + (random.random() * 10 - 5))
    time.sleep(0.001)

