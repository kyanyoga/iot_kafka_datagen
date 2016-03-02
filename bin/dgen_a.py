#!/usr/bin/env python
"""
Created on Sun Feb 21 14:45:34 2016

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
from collections import OrderedDict
from kafka import SimpleProducer, KafkaClient

# kafka server info
# kafka = KafkaClient("localhost")

# producer = SimpleProducer(kafka) 
# topic = b'test' 

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
      
# create dictionary
def create_jmsg(timestamp, timezone, millis, senstype, metric):
    msg = OrderedDict()         # ordered dictionary
    if(timestamp != ""):
        msg["timestamp"] = timestamp
    if(timezone != ""):
        msg["timezone"] = timezone
    if(millis != ""):
        msg["millis"] = millis
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
    #create random values
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
        jmsg = create_jmsg(t,timezone,millis, metric, baseTemp)
    
    if metric == 'currentPresure':
        basePresure = basePresure + sin_value*10
        if basePresure <= 0:
            basePresure = 1000 # reset if sin function takes you negative
        # create message dictionary    
        jmsg = create_jmsg(t,timezone,millis, metric, basePresure)
    
    if metric == 'currentLevel':
        baseLevel =  baseLevel + sin_value*.10
        if baseLevel <= 0:
            baseLevel = 10 
        # create message dictionary    
        jmsg = create_jmsg(t,timezone,millis, metric, baseLevel)
        
    # TODO: Push to Kafka
        
    # sleep to slow down generation
    time.sleep( .7750 / 1000.0 )
    
    # reset values for next cycle
    jmsg = {}
