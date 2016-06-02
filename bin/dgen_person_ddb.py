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
        if baseBodyTemp <= 97.5:
            baseBodyTemp = 98.6  
        if baseBodyTemp >= 101.0:
            baseBodyTemp = 98.6
        # reset if sin function takes you negative
        # create message dictionary    
        jmsg = create_jmsg(t,timezone,millis, "sensor105", metric, baseBodyTemp)
    
    if metric == 'currentHeartRate':
        # keep simulated heartRate in range
        baseHeartRate = baseHeartRate + sin_value*3
        if baseHeartRate <= 40:
            baseHeartRate =  75
        if baseHeartRate >= 190:
            baseHeartRate = 75
        # create message dictionary    
        jmsg = create_jmsg(t,timezone,millis, "sensor106", metric, baseHeartRate)
        
    if metric == 'currentRespiration':
        # keep simulated respiration in range
        baseRespiration = baseRespiration + sin_value*1.5
        if baseRespiration <= 5:
            baseRespiration = 18
        if baseRespiration >= 38:
            baseRespiration = 18
        # create message dictionary    
        jmsg = create_jmsg(t,timezone,millis, "sensor107", metric, baseRespiration)
        
    if metric == 'currentActivityLevel':      
        # keep simulated activity level in range
        baseActivityLevel = baseActivityLevel + sin_value*0.5
        if baseActivityLevel <= 0.5:
            baseActivityLevel = 1.75
        if baseActivityLevel >= 3.0:
            baseActivityLevel = 1.75
        # create map   
        jmsg = create_jmsg(t,timezone,millis, "sensor108", metric, baseActivityLevel)
        
        

    # push data into DynamoDB Table
    table.put_item(
        Item={ 
        "sensortype":jmsg.get("senstype"),
        "sensordatetime":jmsg.get("timestamp")+":"+jmsg.get("millis"),
        "timezone":jmsg.get("timezone"),
        "sensorname":jmsg.get("sensor"),
        "metric": str(jmsg.get("metric"))
        # "tags": ["person", "info", "activity"]
        }
    )
        
    # sleep to slow down generation
    time.sleep( .7750 / 1000.0 )
    # time.sleep(15)
    
    # time.sleep(random.random())
    
    # reset values for next cycle
    jmsg = {}
