#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pyRRD_Redis import RRD_redis
import argparse

# parse args
parser = argparse.ArgumentParser()
parser.add_argument('tag_name', type=str, help='tag name like L1_M_WOBBE')
parser.add_argument('-n', '--number', type=int, help='number of RRD samples from now', default=360)
args = parser.parse_args()

# init RRD db
rrd = RRD_redis('rrd:' + args.tag_name)
# dump database
for rrv in rrd.get(size=args.number):
    print(rrv.time_str + ';' + rrv.value_str)
