# -*- coding: utf-8 -*-
from kafka import SimpleClient, SimpleProducer, KafkaConsumer

kafka = SimpleClient("192.168.6.51  192.168.6.52   192.168.6.53  192.168.6.54  192.168.6.55")
producer = SimpleProducer(kafka)

kafka.close()
