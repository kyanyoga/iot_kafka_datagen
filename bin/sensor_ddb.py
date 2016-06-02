#!/usr/bin/env python
"""
Created on May 19, 2016
@author: Gus Segura
"""
from __future__ import print_function # Python 2/3 compatibility
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")

# partition-shard by lower selectivity - higher generalization
# sorkey by semi-unique idenfifiers 
table = dynamodb.create_table(
    TableName = 'IOTSensorDataSimulated',
    KeySchema=[
        {
            'AttributeName': 'sensortype',
            'KeyType': 'HASH'  #Partition key  
        },
        {
            'AttributeName': 'sensordatetime',
            'KeyType': 'RANGE'  #Sort key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'sensortype',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'sensordatetime',
            'AttributeType': 'S'
        },

    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 1,
        'WriteCapacityUnits': 1
    }    
)

print("Table status:", table.table_status)
