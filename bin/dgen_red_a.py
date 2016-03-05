#!/usr/bin/env python
"""
Created on March 4, 2016
@author: Gus Segura
"""

# imports
import time
import random
import base64
import os
import sys
import math
import json
import redis
from collections import OrderedDict

# redis server connection
# Connection to Database: this is how we work with Redis
database = redis.StrictRedis(host='localhost', port=6379, db=0)

# Output file for testing when not pushing to Kafka, Redis, SparkStreaming.
# pwd = os.path.dirname(__file__)
# print pwd
# outputpath = os.path.normpath(pwd + '/../sample_data/' + sys.argv[1])

# outputpath = os.path.normpath(sys.argv[1])
# outputpath = "file.log"

# print  outputpath

# startng values for simulated sensors
start = time.time()
start_value = 0

baseTemp = 32.0
basePresure = 1000
baseLevel = 10

jmsg = {}

# create new redis cache object : TODO - Migrate Object Creation
def Sensmsg(object):
    """ Holds the model for Sensor Message
    Performs sensor message data storage management using the next data structure:
    
    next-sensor-msg-id: <uid>       - holds the next sensor message id to generate
    
    "sensmsg:<uid>": {
        timestamp:<timestamp>
        timezone:<timezone>
        millisec:<millis>
        sensname:<sensor_name>
        senstype:<sensor_type>
        metric:<value>
    }
    
    """
    pass
      
# create dictionary
def create_jmsg(timestamp, timezone, millis, sensor, senstype, metric):
    msg = OrderedDict()         # ordered dictionary
    if(timestamp != ""):
        msg["timestamp"] = timestamp
    if(timezone != ""):
        msg["timezone"] = timezone
    if(millis != ""):
        msg["millis"] = millis
    if(sensor != ""):
        msg["sensor"] = sensor
    if(senstype != ""):
        msg["senstype"] = senstype
    if(metric != ""):
        msg["metric"] = metric
    print(json.dumps(msg))
    return msg

# main infinite loop
while (True):
    t = time.strftime('%Y-%m-%dT%H:%M:%S')
    timezone = time.strftime('%z')
    millis = "%.3d" % (time.time() % 1 * 1000)
    
    sin_value = math.sin(start_value)
    start_value += 1
    
    #open file for append
    # outputfile = open(outputpath, 'a+')
    
    # sensor name
    #create random values - well match sensor id to type for now.
    sensor = random.sample(['sen/1', 'sen/2', 'sen/3', 'send/4'], 1)[0]
    
    # metric type
    metric = random.sample(['currentTemp', 'currentPresure', 'currentLevel'], 1)[0]
    
    # case -- yuk: python uses if else.
    # -------------------------------- #
    if metric == 'currentTemp':
        baseTemp = baseTemp + sin_value
        if baseTemp <= 0:
            baseTemp = 32.0  # reset if sin function takes you negative
        # create message dictionary    
        jmsg = create_jmsg(t,timezone,millis, "sen/1", metric, baseTemp)
    
    if metric == 'currentPresure':
        basePresure = basePresure + sin_value*10
        if basePresure <= 0:
            basePresure = 1000 # reset if sin function takes you negative
        # create message dictionary    
        jmsg = create_jmsg(t,timezone,millis, "sen/2", metric, basePresure)
    
    if metric == 'currentLevel':
        baseLevel =  baseLevel + sin_value*.10
        if baseLevel <= 0:
            baseLevel = 10 
        # create message dictionary    
        jmsg = create_jmsg(t,timezone,millis, "sen/3", metric, baseLevel)
        
    # TODO: Push to Redis
    msg_id = database.incr("next-senmsg-id")
    print (msg_id)
    
    # "HMSET" allows to set many keys for hash map
    database.hmset("sensmsg:{0}".format(msg_id),
        { 
            "timestamp":jmsg.get("timestamp"),
            "timezone":jmsg.get("timezone"),
            "millisec":jmsg.get("millis"),
            "sensname":jmsg.get("sensor"),
            "senstype":jmsg.get("senstype"),
            "metric":jmsg.get("metric")
        }
    )
        
    # sleep to slow down generation
    time.sleep( .7750 / 1000.0 )
    
    # reset values for next cycle
    jmsg = {}
