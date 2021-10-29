import os   # need this for popen
import time # for sleep
from kafka import KafkaConsumer  # consumer of events
import json
import couchdb
# We can make this more sophisticated/elegant but for now it is just
# hardcoded to the setup I have on my local VMs

# acquire the consumer
# (you will need to change this to your bootstrap server's IP addr)
consumer = KafkaConsumer (bootstrap_servers=["129.114.26.116:9092", "129.114.25.114:9092", "3.90.222.36:9092"])

# subscribe to topic
consumer.subscribe (topics=["china", "andorra", "greece"])

couch = couchdb.Server()
couch.resource.credentials = ('admin', 'cloud-computing')
db_andorra = couch.create('gdp_data_andorra')
db_greece = couch.create('gdp_data_greece')
db_china = couch.create('gdp_data_china')


# we keep reading and printing
for msg in consumer:
    # what we get is a record. From this record, we are interested in printing
    # the contents of the value field. We are sure that we get only the
    # utilizations topic because that is the only topic we subscribed to.
    # Otherwise we will need to demultiplex the incoming data according to the
    # topic coming in.
    #
    # convert the value field into string (ASCII)
    #
    # Note that I am not showing code to obtain the incoming data as JSON
    # nor am I showing any code to connect to a backend database sink to
    # dump the incoming data. You will have to do that for the assignment.
    #print (str(msg.value, 'ascii'))
    # In our Kafka code, the deserialization will be done by the consumer
    # now deserialize and see if it is printing the right thing
    #print ("deserialize the topic")
    #start_time = time.time ()
    #retrieved_topic = json.loads (buf)
    retrieved_topic = json.loads (msg.value)
    #end_time = time.time ()
    #print ("Deserialization took {} secs".format (end_time-start_time))

    print ("Deserialized obj = {}\n".format (retrieved_topic))

    if retrieved_topic['name'] == 'Andorra GDP per Capita':
        db_andorra.save(retrieved_topic)
    elif retrieved_topic['name'] == 'China GDP per Capita':
        db_china.save(retrieved_topic)
    elif retrieved_topic['name'] == 'Greece GDP per Capita':
        db_greece.save(retrieved_topic)

# we are done. As such, we are not going to get here as the above loop
# is a forever loop.
consumer.close ()
