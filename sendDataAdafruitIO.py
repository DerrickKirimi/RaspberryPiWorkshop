import network
import socket
from time import sleep
import machine
from umqtt.simple import MQTTClient
import random
import ahtx0
from machine import Pin, I2C

i2c = I2C(1, scl=Pin(15), sda=Pin(14))
sensor = ahtx0.AHT10(i2c)

import wificonnect
print("Connected to Wifi.")

mqtt_server = 'io.adafruit.com'
mqtt_port = 1883 # non-SSL port
mqtt_user = 'Dr3co' #Adafruit ID
mqtt_password = 'aio_rJAo04Q8J6tUsRPdocvymy6os5Lz' # Under Keys
mqtt_topic = 'Dr3co/feeds/temperature' # Under "Feed info"
mqtt_client_id = str(random.randint(10000,999999)) #must have a unique ID - good enough for now

i2c = I2C(1, scl=Pin(15), sda=Pin(14))
sensor = ahtx0.AHT10(i2c)


def mqtt_connect():
    client = MQTTClient(client_id=mqtt_client_id, server=mqtt_server, port=mqtt_port, user=mqtt_user, password=mqtt_password, keepalive=3600)
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_server))
    return client

def reconnect():
    print('Failed to connect to the MQTT Broker. Reconnecting...')
    time.sleep(5)
    reset()

try:
    client = mqtt_connect()
except OSError as e:
    reconnect()
    
while True:
    wlan = network.WLAN(network.STA_IF)
    if wlan.isconnected():
        temp = str(round(sensor.temperature,1))
        client.publish(mqtt_topic, temp)
        print("Sent temp value: " + temp)
    else:
        reconnect()
    sleep(20)