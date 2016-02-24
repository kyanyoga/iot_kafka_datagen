# Consumer example to show the producer works: J.Oxenberg
from kafka import KafkaConsumer 
consumer = KafkaConsumer(b'test',bootstrap_servers="172.17.136.43") 
#wait for messages 
for message in consumer: 
    print(message) 
