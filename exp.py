import asyncio
from bleak import BleakClient, BleakScanner
import binascii
import logging

DEVICE_ADDRESS = "C4:AC:60:E0:75:95"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def explore_services(client):
    for service in client.services:
        logger.info("[Service] %s", service)

        for char in service.characteristics:
            if "read" in char.properties:
                try:
                    value = await client.read_gatt_char(char.uuid)
                    extra = f", Value: {value}"
                except Exception as e:
                    extra = f", Error: {e}"
            else:
                extra = ""

            if "write-without-response" in char.properties:
                extra += f", Max write w/o rsp size: {char.max_write_without_response_size}"

            logger.info(
                "  [Characteristic] %s (%s)%s",
                char,
                ",".join(char.properties),
                extra,
            )

            for descriptor in char.descriptors:
                try:
                    value = await client.read_gatt_descriptor(descriptor.handle)
                    logger.info("    [Descriptor] %s, Value: %r", descriptor, value)
                except Exception as e:
                    logger.error("    [Descriptor] %s, Error: %s", descriptor, e)


async def battery_level(client):
    uuid = "00000008-0000-1000-8000-00805f9b34fb"
    out = await client.read_gatt_char(uuid)
    logger.info(f"Received: {out}, {binascii.hexlify(out)}")
    

    return {
        "left": out[0],
        "right": out[1],
    }
        

async def main(address):
    logger.info(f"Connecting to device: {address}")

    async with BleakClient(address) as client:
        if client.is_connected:
            logger.info(f"Connected: {client}")


        #await explore_services(client)
        logger.info(await battery_level(client))


asyncio.run(main(DEVICE_ADDRESS))
