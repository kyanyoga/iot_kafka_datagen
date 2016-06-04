# iot_kafka_datagen
## The following App will generate sample IOT data and push to Kafka, Redis and Now AWS DynamoDB. ##
### The data will follow a predicable pattern so that it can be replicated. ###
** Using a sin wave function will vary temperature, bp and activity over time **

** added a redis output file so we can pick out desitination **

** added specific generator for person data **

** added specific generator for machine data **

## Latest: May 2016  
### Note: You will need to install AWS Cli, Boto3 (for Python) and Most likely DynamoDB locally to Test.
### Added new DynamoDB Data Generator
1) download and install DynamoDB local (easy) -or- change end point in scripts.
#### [sensor_ddb.py, dgen_person_ddb.py, dgen_mach_ddb.py] to your DynamoDB end-point.
#### You will also need to configure AWS CLI with your keys and default region.
#### http://docs.aws.amazon.com/general/latest/gr/rande.html

2) run the ddb table build script: user$ python sensor_ddb.py  [ This will build the IOT Sensor Table ].

3) run the desired generator: 
* a) user$ python dgen_person_ddb.py  [ generate person data to ddb ] - or -
* b) user$ python dgen_mach_ddb.py    [ generate machine data to ddb ]
