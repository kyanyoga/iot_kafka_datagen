#!/usr/bin/env python
"""
Created on March 4, 2016
Updated on May 18, 2016
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

baseBodyTemp = 98.6
baseHeartRate = 75
baseBloodPressure = [120,80]
baseRespiration = 18
baseActivityLevel = 1.75 
    

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

# data changer
def data_changer(sensor_type, base_value, multiplier):
    pass


# main infinite loop
while (True):
    t = time.strftime('%Y-%m-%dT%H:%M:%S')
    timezone = time.strftime('%z')
    millis = "%.3d" % (time.time() % 1 * 1000)
    
    sin_value = math.sin(start_value)
    start_value += 1
    
    # open file for append
    # outputfile = open(outputpath, 'a+')
        
    # metric type
#    metric = random.sample(['currentBodyTemp', 'currentHeartRate', 'currentBloodPressure', 'currentRespiration', 'currentActivityLevel'], 1)[0]
    metric = random.sample(['currentBodyTemp', 'currentHeartRate', 'currentRespiration', 'currentActivityLevel'], 1)[0]
    
    # case -- yuk: python uses if else. 
    # -------------------------------- #
    if metric == 'currentBodyTemp':  # print (100 + math.sin(x)*10)
        # keep simulated bodyTemp in range
        baseBodyTemp = baseBodyTemp + sin_value*1.5
        if baseBodyTemp <= 95.0:
            baseBodyTemp = 95.0  
        if baseBodyTemp >= 115.0:
            baseBodyTemp = 104.0
        # reset if sin function takes you negative
        # create message dictionary    
        jmsg = create_jmsg(t,timezone,millis, "sensTemp", metric, baseBodyTemp)
    
    if metric == 'currentHeartRate':
        # keep simulated heartRate in range
        baseHeartRate = baseHeartRate + sin_value*3
        if baseHeartRate <= 40:
            baseHeartRate =  75
        if baseHeartRate >= 190:
            baseHeartRate = 75
        # create message dictionary    
        jmsg = create_jmsg(t,timezone,millis, "senHeartRate", metric, baseHeartRate)
        
    if metric == 'currentRespiration':
        # keep simulated respiration in range
        baseRespiration = baseRespiration + sin_value*1.5
        if baseRespiration <= 5:
            baseRespiration = 18
        if baseRespiration >= 38:
            baseRespiration = 18
        # create message dictionary    
        jmsg = create_jmsg(t,timezone,millis, "senResp", metric, baseRespiration)
        
    if metric == 'currentActivityLevel':      
        # keep simulated activity level in range
        baseActivityLevel = baseActivityLevel + sin_value*0.5
        if baseActivityLevel <= 0.5:
            baseActivityLevel = 1.75
        if baseActivityLevel >= 3.0:
            baseActivityLevel = 1.75
        # create map   
        jmsg = create_jmsg(t,timezone,millis, "senActivity", metric, baseActivityLevel)
        
        
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
    # time.sleep(15)
    
    # time.sleep(random.random())
    
    # reset values for next cycle
    jmsg = {}
