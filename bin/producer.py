# Kafka Producer - J. Oxenberg
from faker import Factory 
from kafka import SimpleProducer, KafkaClient 
fake = Factory.create() 
kafka = KafkaClient("172.17.136.43") 
producer = SimpleProducer(kafka) 
topic = b'test' 
#generate list of tuples to send via kafka, (timestamp, geo-coordinate) (mimics a sensor value) 
x = [(fake.iso8601(),fake.geo_coordinate()) for x in range(10)] 
for t in x: 
#this is where the message gets sent. It needs to be sent as bytes 
    producer.send_messages(topic, str.encode(str(t))) 
