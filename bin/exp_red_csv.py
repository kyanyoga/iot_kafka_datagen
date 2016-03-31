#!/usr/bin/env python
"""
Created on March 30, 2016
@author: Gus Segura
"""

# imports
import time
import os
import sys
import redis
import csv


""" define objects """

outputpath = os.path.normpath(sys.argv[1])
        
def main():
    """ Set up the main game loop """
    # locals
    write_header = False
    
    # redis server connection
    # Connection to Database: this is how we work with Redis
    database = redis.StrictRedis(host='localhost', port=6379, db=0)
    
    # check if file is there
    if not os.path.isfile(outputpath):
        write_header = True
        # print 'file not here...'
        
    # open file for append
    # outputfile = open(outputpath, 'wt')    
    outputfile = open(outputpath, 'a+')
    
    writer =  csv.writer(outputfile)
    
    # write header for new file
    if write_header:
        writer.writerow( ('Datetime', 'Timezone', 'Millisec', 'Sensname', 'Senstype', 'Metric'))
    
    # get counter value
    counter  = database.get("next-senmsg-id")
    
    """ maybe use 2 loops one to get latest counter value and a second to clear the cache """
    # one loop seems to be fine
    while ( counter >= 0 ):
        
        # get the data
        data = database.hmget("sensmsg:{0}".format(counter), "timestamp", "timezone", "millisec", "sensname", "senstype", "metric")
            
        # print the data
        print data
        
        # write to csv
        # writer.writerow( (i+1, chr(ord('a') + i), '08/%02d/07' % (i+1)) )
        writer.writerow((data[0], data[1], data[2], data[3], data[4], data[5]))
        
        """ delete the old data : maybe use a clean up for this"""
        # get counter value
        counter  = database.decr("next-senmsg-id")  
        
    print "Leaving..."
    database.set("next-senmsg-id", 0)
    outputfile.close()
        
"""call main"""        
main()
