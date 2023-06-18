import paho.mqtt.client as mqtt
import threading
from time import sleep

# define static variable
# broker = "localhost" # for local connection
broker = "test.mosquitto.org"  # for online version
port = 1883
timeout = 60

username = ''
password = ''

topic = "nurrizal/182"
topic_pub = "nurrizal/182/greetings"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc)+" topic: "+ client.topic)
 
    # Subscribing in on_connect() - if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(client.topic,qos=2)
        
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if client.topic_pub == '':
        print("response from "+msg.topic+" "+str(msg.payload.decode('utf-8'))+"\n")
    message = str(msg.payload.decode('utf-8'))
    if client.topic_pub != '':
        ret = client.publish(client.topic_pub,payload=message,qos=1)
        print(f"data published to {client.topic_pub}\n")

# Create an MQTT client and attach our routines to it.

def publish(topic, topic_pub):
    client = mqtt.Client("nurrizal/device1")
    client.topic = topic
    client.topic_pub = topic_pub
    client.username_pw_set(username=username,password=password)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, port, timeout)
    client.loop_forever()

def greetings(topic):
    client = mqtt.Client("nurrizal/device2")
    client.topic = topic
    client.topic_pub = ''
    client.username_pw_set(username=username,password=password)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, port, timeout)
    client.loop_forever()

try:
    t1 = threading.Thread(target=publish, args=(topic,topic_pub))
    t2 = threading.Thread(target=greetings, args=(topic_pub,))
    t1.daemon = True
    t2.daemon = True
    t1.start()
    t2.start()
    while True:
        sleep(1)
except(KeyboardInterrupt, SystemExit):
    print('Received keyboard interrupt, quitting threads.')