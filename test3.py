import asyncio
import logging
import os

from hbmqtt.client import MQTTClient
from hbmqtt.mqtt.constants import QOS_0, QOS_1, QOS_2

# Set up logging
logging.basicConfig(level=logging.INFO)

async def subscribe_coro():
    C = MQTTClient()
    await C.connect('mqtt://localhost/')
    await C.subscribe([
        ('topic1', QOS_0),
        ('topic2', QOS_1),
        ('topic3', QOS_2),
    ])
    try:
        while True:
            message = await C.deliver_message()
            packet = message.publish_packet
            print(f"Received message: {packet.payload.decode()}")
    finally:
        await C.unsubscribe(['topic1', 'topic2', 'topic3'])
        await C.disconnect()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(subscribe_coro())