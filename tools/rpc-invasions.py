#!/usr/bin/python

from jsonrpclib import Server
import time
import random
import json
import math
import os
from Crypto.Cipher import AES
import base64
import sys


RPC_SERVER_SECRET = sys.argv[1]

client = Server(sys.argv[2])

def generate_token(accessLevel):
    """
    Generate an RPC server token with the given access level.
    """
    token = {'timestamp': int(time.mktime(time.gmtime())), 'accesslevel': accessLevel}
    data = json.dumps(token)
    iv = os.urandom(AES.block_size)
    cipher = AES.new(RPC_SERVER_SECRET, mode=AES.MODE_CBC, IV=iv)
    data += '\x00' * (16 - (len(data)%AES.block_size))
    token = cipher.encrypt(data)
    return base64.b64encode(iv + token)

random.seed()
while True:
  try:
    res = client.ping(generate_token(700), 12345)
    if res != 12345:
      print "Is the server accessable?\n"
      exit
    
    # How many times a day is this script going to be called?
    ChecksPerDay = 60.0*24.0    # Once a minute
    InvasionsPerDay = 72.0      # How many invasions a day per district
    BaseInvasionChance = InvasionsPerDay/ChecksPerDay
    
    safeHarbor = {'Wacky Woods'}
    superDistricts = {'Roaring Rivers'}
    
    
    while True:
      shards = client.listShards(generate_token(700))
      print shards
      count = 0
      for skey in shards:
        shard = shards[skey]
        if shard['invasion'] != None:
          count = count + 1
      for skey in shards:
        shard = shards[skey]
        if shard['invasion'] == None:
          if shard['name'] in superDistricts:
            typ = int(float(random.random()) * 4.0)
            suit = int(float(random.random()) * 4.0) + 4  # Bias the cogs to be big
            client.startInvasion(generate_token(700), int(skey), typ, suit, 0, 0)
            count = count + 1
            print 'Calling invasion for %s with %d,%d'%(shard['name'],typ,suit)
      if count < 3:
        for skey in shards:
          shard = shards[skey]
          if shard['invasion'] == None and not shard['name'] in safeHarbor:
            r = random.random()
            if r < BaseInvasionChance and not shard['name'] in superDistricts:
              typ = int(float(random.random()) * 4.0)
              suit = int(float(random.random()) * 8.0)
              client.startInvasion(generate_token(700), int(skey), typ, suit, 0, 0)
              print 'Calling invasion for %s with %d,%d'%(shard['name'],typ,suit)
      print "tick..(was %d)\n"%(count)
      time.sleep(60)
  except Exception, e:
    print e
  time.sleep(300)
