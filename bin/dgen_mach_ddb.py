#!/usr/bin/env python

from __future__ import print_function # Python 2/3 compatibility
import time
import random
import base64
import os
import sys
import math
import json
import redis
import boto3
import os
from collections import OrderedDict

"""
Created on May 19, 2016
@author: Gus Segura
"""

# connect to ddb and table
dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
table = dynamodb.Table('IOTSensorDataSimulated')

# startng values for simulated sensors
start = time.time()
start_value = 0

baseTemp = 32.0
basePresure = 1000
baseLevel = 10
baseVoltage = 220

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
    # sensor = random.sample(['sen/1', 'sen/2', 'sen/3', 'sen/4'], 1)[0]
    
    # metric type
    metric = random.sample(['currentTemp', 'currentPresure', 'currentLevel', 'currentVoltage'], 1)[0]
    
    # case -- yuk: python uses if else.
    # -------------------------------- #
    if metric == 'currentTemp':
        baseTemp = baseTemp + sin_value
        if baseTemp <= 0:
            baseTemp = 32.0  # reset if sin function takes you negative
        # create message dictionary    
        jmsg = create_jmsg(t,timezone,millis, "sensor101", metric, baseTemp)
    
    if metric == 'currentPresure':
        basePresure = basePresure + sin_value*10
        if basePresure <= 0:
            basePresure = 1000 # reset if sin function takes you negative
        # create message dictionary    
        jmsg = create_jmsg(t,timezone,millis, "sensor102", metric, basePresure)
    
    if metric == 'currentLevel':
        baseLevel =  baseLevel + sin_value*.10
        if baseLevel <= 0:
            baseLevel = 10 
        # create message dictionary    
        jmsg = create_jmsg(t,timezone,millis, "sensor103", metric, baseLevel)
        
    if metric == 'currentVoltage':
        baseVoltage =  baseVoltage + sin_value*1.5
        if baseVoltage <= 0:
            baseVoltage = 220
        if baseVoltage >= 225:
            baseVoltage = 220
        # create message dictionary    
        jmsg = create_jmsg(t,timezone,millis, "sensor104", metric, baseVoltage)
    
         
    # TODO: Create Unique Message ID if needed
    # msg_id = database.incr("next-senmsg-id")
    # print (msg_id)
    
    table.put_item(
        Item={ 
        "sensortype":jmsg.get("senstype"),
        "sensordatetime":jmsg.get("timestamp")+":"+jmsg.get("millis"),
        "timezone":jmsg.get("timezone"),
        "sensorname":jmsg.get("sensor"),
        "metric": str(jmsg.get("metric"))
        #"tags": ["machine", "info", "maintenance"]
        }
    )
        
    # sleep to slow down generation
    time.sleep( .7750 / 1000.0 )
    
    # time.sleep(random.random())
    
    # reset values for next cycle
    jmsg = {}
