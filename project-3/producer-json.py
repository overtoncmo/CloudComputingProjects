#
#
# Author: Aniruddha Gokhale, Matthew Tremblay
# CS4287-5287: Principles of Cloud Computing, Vanderbilt University
#
# Created: Sept 6, 2020
# Modified Sept 20, 2021
#
# Purpose:
#
#    Demonstrate the use of Kafka Python streaming APIs.
#    In this example, we use the "top" command and use it as producer of events for
#    Kafka. The consumer can be another Python program that reads and dumps the
#    information into a database OR just keeps displaying the incoming events on the
#    command line consumer (or consumers)
#

import time # for sleep
import json # for serialization
from kafka import KafkaProducer  # producer of events

# We can make this more sophisticated/elegant but for now it is just
# hardcoded to the setup I have on my local VMs

# acquire the producer
# (you will need to change this to your bootstrap server's IP addr)
producer = KafkaProducer (bootstrap_servers="129.114.25.114:9092")
#                                                  acks=1)  # wait for leader to write to log
f = open("GDP_per_capita.csv")
lines = f.readlines()
f.close()
data_andorra = list(map(float, lines[1].split(',')[5:]))
years = list(map(lambda x: int(x.split()[0]), lines[0].split(',')[5:]))
# We call it a topic so we can relate it to the topic data that we want
# to send to Kafka
topic = {"seqnum": -1,
         "name": "Andorra GDP per Capita",
         "ts": 0,
         "year": -1,
         "GDP": 0.0
         }

# say we send the contents 100 times after a sleep of 1 sec in between
for i in range (len(data_andorra)):
    # fill the seq num and timestamp
    topic ["seqnum"] = i
    topic["ts"] = time.time ()

    topic["year"] = years[i]
    topic["GDP"] = data_andorra[i]

    # get a serialized buffer with seq num and some data items
    # In our Kafka code, the serialization will be done by the producer
    print ("Iteration #{}".format (i))
    print ("Serialize")

    # Note that JSON will convert things into string. Moreover, it can
    # do this for all known types. For anything beyond this, one must supply
    # an encoder
    start_time = time.time ()
    buf = json.dumps (topic)
    end_time = time.time ()
    print ("Serialization took {} secs".format (end_time-start_time))
#'''
    # In our Kafka code, the deserialization will be done by the consumer
    # now deserialize and see if it is printing the right thing
    print ("deserialize the topic")
    start_time = time.time ()
    retrieved_topic = json.loads (buf)
    end_time = time.time ()
    print ("Deserialization took {} secs".format (end_time-start_time))

    print ("Deserialized obj = {}".format (retrieved_topic))
#'''
    # send the contents under topic utilizations. Note that it expects
    # the contents in bytes so we convert it to bytes.
    #
    # Note that here I am not serializing the contents into JSON or anything
    # as such but just taking the output as received and sending it as bytes
    # You will need to modify it to send a JSON structure, say something
    # like <timestamp, contents of top>
    #
    producer.send ("utilizations", value=bytes (buf, 'ascii'))
    producer.flush ()   # try to empty the sending buffer

    # sleep a second
    time.sleep (0.5)

    # we are done
producer.close ()
