# iot_kafka_datagen
## The following App will generate sample IOT data and push to Kafka ( and Redis ). ##
### The data will follow a predicable pattern so that it can be replcated. ###
** Using a sin wave function will vary temperature, bp and activity over time **

** added a redis output file so we can pick out desitination **

** added specific generator for person data **

** added specific generator for machine data **

## May 2016 ##
## Added new DynamoDB Data Generator ##
1) download and install DynamoDB local or change end point in : sensor_ddb.py, dgen_person_ddb.py, dgen_mach_ddb.py
2) run the table build script: user$ python sensor_ddb_py
3) run the desired generator: user$ python dgen_person_ddb.py  -or- user$ python dgen_mach_ddb.py
