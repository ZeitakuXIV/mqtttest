import paho.mqtt.client as paho
from paho import mqtt
from time import sleep

# define static variable
# broker = "localhost" # for local connection
broker = "test.mosquitto.org"  # for online version
port = 1883
timeout = 60

username = ''
password = ''
topic = "nurrizal/182"
topic_sub = "nurrizal/182/greetings"
nama = "Nurrizal"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
def on_publish(client,userdata,result):
	print("data published \n")


client1 = paho.Client("nurrizal/device0",userdata=None,protocol=paho.MQTTv5)
client1.username_pw_set(username=username,password=password)
client1.on_connect = on_connect
client1.on_publish = on_publish
client1.connect(broker,port,timeout)

while True:
	message = f"Hallo selamat siang, {nama}."
	ret = client1.publish(topic,payload=message,qos=1)
	sleep(1)




