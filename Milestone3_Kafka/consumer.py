from kafka import KafkaConsumer
from json import loads

consumer = KafkaConsumer(
    'final_project',
     bootstrap_servers=['localhost:9092'],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='my-group',
     value_deserializer=lambda x: x.decode('utf-8'))

for message in consumer:
    print(message)
