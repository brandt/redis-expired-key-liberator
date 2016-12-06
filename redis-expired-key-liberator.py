#!/usr/bin/env python

# Finds all expired keys in a Redis RDB database and performs a GET
# operation on them, which cues Redis to garbage collect the item.
#
# Requirements:
#
#     pip install rdbtools
#     pip install redis
#

import os
import sys
import datetime
import redis
from rdbtools import RdbParser, RdbCallback

class KeyCallback(RdbCallback) :
  """
  Calls method for every item found when a method for said item exists.
  """

  def __init__(self):
    self.now = datetime.datetime.now()
    self.redis = redis.Redis(unix_socket_path='/tmp/redis.sock')
    # self.redis = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
    self.counter = 0

  def set(self, key, value, expiry, info):
    if expiry is not None:
      if expiry <= self.now:
        #print 'Found expired key: %s' % str(key)
        self.redis.get(str(key))
        self.counter += 1
        if self.counter % 1000 == 0:
          print self.counter


def main():
  """
  Usage: redis-expired-key-liberator [rdb_path]
  """

  print len(sys.argv)

  if len(sys.argv) == 1:
    rdb_path = '/var/lib/redis/dump-master.rdb'
  elif len(sys.argv) == 2:
    rdb_path = sys.argv[1]
  else:
    print 'Usage: redis-expired-key-liberator [rdb_path]'
    exit(2)

  if not os.path.isfile(rdb_path):
    print "Error: could not read file:", rdb_path
    exit(1)

  callback = KeyCallback()
  parser = RdbParser(callback)
  parser.parse(rdb_path)


if __name__ == "__main__":
  main()
