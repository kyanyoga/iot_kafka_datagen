#!/usr/bin python 

import time
import random
import base64
import os
import sys

start = time.time()

# pwd = os.path.dirname(__file__)
# outputpath = os.path.normpath(pwd + '/../sample_data/' + sys.argv[1])

outputpath = os.path.normpath(sys.argv[1])
# print  outputpath

#run for five minutes
# while time.time() < start + 300:
    
#run forever
while (True):
    t = time.strftime('%Y-%m-%dT%H:%M:%S')
    timezone = time.strftime('%z')
    millis = "%.3d" % (time.time() % 1 * 1000)
    
    #open file for append
    outputfile = open(outputpath, 'a+')

    #create random values
    level = random.sample(['DEBUG', 'INFO', 'WARN', 'ERROR'], 1)[0]
    message = random.sample(['Don\'t worry, be happy.',
                             'error, ERROR, Error!',
                             'Nothing happened. This is worthless. \
                              Don\'t log this.',
                             'Hello world.'], 1)[0]

    logger = random.sample(['FooClass',
                            'BarClass',
                            'AuthClass',
                            'LogoutClass',
                            'BarClass',
                            'BarClass',
                            'BarClass',
                            'BarClass'], 1)[0]

    user = random.sample(['jeff',
                          'mo',
                          'aaron',
                          'rajesh',
                          'sunil',
                          'zach',
                          'gus'], 1)[0]

    ip = random.sample(['1.2.3.4',
                        '4.31.2.1',
                        '1.2.3.',
                        '1.22.3.3',
                        '3.2.4.5',
                        '113.2.4.5'], 1)[0]

    req_time = str(int(abs(random.normalvariate(0, 1)) * 1000))
    session_length = str(random.randrange(1, 12240))
    session_id = base64.b64encode(str(random.randrange(1000000, 1000000000)))
    extra = random.sample(['network=qa',
                           'network=prod',
                           'session_length=' + session_length,
                           'session_id="' + session_id + '"',
                           'user=extrauser'], 1)[0]

    fields = []
    fields.append('logger=' + logger)
    fields.append('user=' + user)
    fields.append('ip=' + ip)
    fields.append('req_time=' + req_time)
    fields.append(extra)

    fields.pop(random.randrange(0, len(fields)))
    
    # print to screen
#    print "%s.%s%s %s %s [%s]" % (t,
#                                  millis,
#                                  timezone,
#                                  level,
#                                  message,
#                                  ", ".join(fields))
    
    # print to file                              
    outputfile.write( "%s.%s%s %s %s [%s]\n" % (t,
                                  millis,
                                  timezone,
                                  level,
                                  message,
                                  ", ".join(fields)))
    outputfile.close()
    #print newline

    # time.sleep(random.random())
