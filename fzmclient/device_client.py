#!/usr/bin/env python
import pika
import sys
import time
import json 

echange = "data"
routing_key =".data.coffee"

# comando per pubblicare: mosquitto_pub -h 
# hostname: mqtt.zerinth.com -u mqtt -P mqtt -t "j/up"  -m 'Hello'
# (user mqtt, password mqtt)

# par  = pika.ConnectionParameters(host='localhost')

credentials = pika.PlainCredentials('admin', 'Z3rynthT3st')
parameters = pika.ConnectionParameters('127.0.0.1',
                                       5672,
                                       '/',
                                       credentials)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.exchange_declare(exchange=echange, exchange_type='topic', durable=True)

for x in range(2000):
    time.sleep(2)
    json_body = {'temp': x, 'rating': 3.5}
    msg = json.dumps(json_body)
    channel.basic_publish( exchange=echange, routing_key=routing_key, body=msg)
    print(" [device client] Sent to exchange: {} msg: {}".format(routing_key, msg))
connection.close()