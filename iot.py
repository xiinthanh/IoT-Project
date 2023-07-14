import sys
import time
from random import randint
from Adafruit_IO import MQTTClient


AIO_USERNAME = "DiscreteGroup"
# AIO_KEY is saved in aio_key.txt
AIO_KEY = open("aio_key.txt", "r").read()

AIO_FEED_ID = ["device-switch"]

COLLECTING = True

# IoT
def connected(client):
    print("Server connected ...")
    for FEED_ID in AIO_FEED_ID:
        client.subscribe(FEED_ID)

def subscribe(client, userdata, mid, granted_qos):
    print("Subscribed...")

def disconnected(client):
    print("Disconnected from the server...")
    sys.exit (1)

def message(client, feed_id, payload):
    print("Received data: " + payload)
    if feed_id == "device-switch":
        if payload == "1":
            COLLECTING = True
        else:
            COLLECTING = False


client = MQTTClient(AIO_USERNAME , AIO_KEY)

client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe

client.connect()
client.loop_background()

# Auto collect data when connect to the server. 
client.publish("device-switch", "1")

while True:
    if not COLLECTING:
        continue

    wind_speed = randint(0, 100)
    client.publish("wind-speed", wind_speed)

    temperature = randint(0, 50)
    client.publish("temperature", temperature)

    humidity = randint(0, 100)
    client.publish("humidity", humidity)

    # Generating random wind direction.
    wind_directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    wind_direction = wind_directions[randint(0, 7)]
    client.publish("wind-direction", wind_direction)

    # Categories: https://www.researchgate.net/figure/Various-categories-of-rainfall-events-and-respective-rainfall-intensity-ranges-as-defined_tbl2_342165818
    # Range: [0.0 - 300.0]
    rainfall_amount = randint(0, 3000) / 10
    client.publish("rainfall", str(rainfall_amount) + " mm/day")
    
    time.sleep(5)
    