#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from redis import StrictRedis, WatchError
import struct
import time
from enum import Enum


class RRD_value(object):
    def __init__(self, value=0.0, timestamp=None, from_str=''):
        self.value = value
        # default timestamp is now
        if timestamp is None:
            self.timestamp = time.time()
        else:
            self.timestamp = timestamp
        # load RRD record from binary string
        if from_str:
            self.load(from_str)

    @property
    def value_str(self):
        return str(self.value)

    @property
    def time_str(self):
        return self.get_str_time()

    def get_str_time(self, fmt='%Y-%m-%d %H:%M:%S', gmt=False):
        if gmt:
            return time.strftime(fmt, time.gmtime(self.timestamp))
        else:
            return time.strftime(fmt, time.localtime(self.timestamp))

    def load(self, s):
        (self.timestamp, self.value) = struct.unpack('df', s)

    def dump(self):
        return struct.pack('df', self.timestamp, self.value)

    def __repr__(self):
        return 'RRD_value(value=%f, timestamp=%f, time_str=%s)'\
               % (self.value, self.timestamp, self.time_str)


class StepAddFunc(Enum):
    min = 1
    max = 2
    avg = 3
    last = 4


class RedisDefault(object):
    client = StrictRedis()


class RRD_redis(object):
    VAL_ARRAY_MAX_SIZE = 1000

    def __init__(self, name, size=7200, step=1.0, add_func=StepAddFunc.avg, client=RedisDefault.client):
        """
        Init an RRD_redis

        :param name: redis tag name for this RRD
        :type name: str
        :param size: RRD max number of record (default is 7200: 2h with 1s step)
        :type size: int
        :param step: minimal number of second between two RRD record (use only with add_step())
        :type step: float
        :param add_func: type of function for use when add_step add a record (min, max, avg...)
        :type add_func: StepAddFunc
        :param client: optional redis client object (for use custom value)
        :type client: redis.client.StrictRedis
        :return: an RRD_redis object
        :rtype: RRD_redis
        """
        # public
        self.name = name
        self.size = size
        self.step = step
        self.add_func = add_func
        # private
        self._c_val = []
        self._r = client

    @property
    def db_name(self):
        return 'rrd:' + self.name if self.name else ''

    def add(self, value, at_time=None):
        """
        Insert value to RRD db and remove the older one

        :param value: value to insert in RRD
        :type value: float
        :param at_time: timestamp for value (default is time.time())
        :type at_time: float
        """
        with self._r.pipeline() as pipe:
            while True:
                try:
                    # watch no change occur on this RRD during add() update
                    pipe.watch(self.db_name)
                    # insert at first position
                    pipe.lpush(self.db_name, RRD_value(value=value, timestamp=at_time).dump())
                    # ensure DB size keep <= max size
                    pipe.ltrim(self.db_name, 0, self.size - 1)
                    pipe.execute()
                    # exit, update is atomic
                    break
                except WatchError:
                    # if RRD change during update just redo it
                    continue

    def add_step(self, value):
        """
        Insert value to RRD db and remove the older one, do this at regular step interval

        :param value: value to insert in RRD
        :type value: float
        """
        # read last insert time
        last_rrv = self.get(size=1, from_last=0)
        if last_rrv:
            ins_time = last_rrv[0].timestamp
        else:
            ins_time = 0.0
        # add current value to values array
        if len(self._c_val) <= RRD_redis.VAL_ARRAY_MAX_SIZE:
            self._c_val.append(value)
        # if "step time" add value to RRD db
        if time.time() >= ins_time + self.step:
            if self.add_func is StepAddFunc.min:
                self.add(min(self._c_val))
            elif self.add_func is StepAddFunc.max:
                self.add(max(self._c_val))
            elif self.add_func is StepAddFunc.avg:
                self.add(sum(self._c_val)/len(self._c_val))
            elif self.add_func is StepAddFunc.last:
                self.add(value)
            self._c_val.clear()

    def get(self, size=0, from_last=0):
        """
        Return a list of RRD_value

        :param size: number of RRD value to retrieve (default is all records)
        :type size: int
        :param from_last: RRD start position (0 for the last inserted value)
        :type from_last: int
        :return: list of RRD_value
        :rtype: list
        """
        # default size is all RRD
        if size == 0:
            size = self._r.llen(self.db_name)
        # format and return array of RRD_value
        ret_l = []
        for s in self._r.lrange(self.db_name, from_last, from_last + size - 1):
            ret_l.append(RRD_value(from_str=s))
        return ret_l

    def rm(self):
        """
        Remove all record from the RRD
        """
        self._r.delete(self.db_name)

    def ls(self):
        """
        List all RRDs available (return tag names)

        :return: list of tag names
        :rtype: list
        """
        l_tag = []
        for tag in self._r.keys('rrd:*'):
            l_tag.append(tag.decode('utf-8')[4:])
        return l_tag

    def __len__(self):
        """
        Get current size of the RRD

        :return: number of items in RRD
        :rtype: int
        """
        return self._r.llen(self.db_name)
