import asyncio
import enum
from typing import Optional
from bleak import BleakClient
import binascii
import logging


DEVICE_ADDRESS = "C4:AC:60:E0:75:95"
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
SERVICE = None


class CommandsEnum(enum.IntEnum):
    ANCSETTING = 23
    BALANCE = 22
    CLEAR_PAIR = 2
    COMPACTNESS = 17
    DIYANSHI = 9
    FACTORY_RESET = 3
    JIANTING = 10
    LEDMODE = 18
    LIGHT = 5
    MUSICACTION = 4
    NOISE = 7
    NOISEMODE = 12
    PAIRLIST = 28
    PAIRNAME = 24
    REQUESTDATA = -2
    RESET_DEFAULT = 1
    RUER = 6
    SLEEPMODE = 16
    TESTMODE = 13
    VOICE = 8
    VOICENAME = 25


async def get_service(client: BleakClient):
    global SERVICE

    if SERVICE:
        return SERVICE
    service_uuid = "0000a001-0000-1000-8000-00805f9b34fb"
    (SERVICE,) = (s for s in client.services if s.uuid == service_uuid)
    return SERVICE


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
                extra += (
                    f", Max write w/o rsp size: {char.max_write_without_response_size}"
                )

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


async def battery_level(client: BleakClient):
    uuid = "00000008-0000-1000-8000-00805f9b34fb"
    out = await client.read_gatt_char(uuid)
    logger.info(f"Received: {out}, {binascii.hexlify(out)}")

    return {
        "left": out[0],
        "right": out[1],
    }


async def get_firmware_version(client: BleakClient):
    uuid = "00000007-0000-1000-8000-00805f9b34fb"
    service = await get_service(client)
    char = service.get_characteristic(uuid)
    if not char:
        logger.error("Characteristic not found")
        return

    out = await client.read_gatt_char(char)
    logger.info(f"Received: {out}, {binascii.hexlify(out)}")

    return out.decode()


async def read_earbud_setting(client: BleakClient):
    uuid = "00001002-0000-1000-8000-00805f9b34fb"
    service = await get_service(client)
    char = service.get_characteristic(uuid)
    if not char:
        logger.error("Characteristic not found")
        return

    out = await client.read_gatt_char(char)
    logger.info(f"Received: {out}, {binascii.hexlify(out)}")


class DataBean:
    @staticmethod
    def get_data_bean(i: int, b_arr: Optional[bytearray]):
        # This method should be implemented to return the appropriate instance
        # based on the value of 'i' and 'b_arr'.
        return {
            "command": CommandsEnum(i),
            "data": b_arr,
        }


def process_byte_array(b_arr):
    array_list = []
    if b_arr is not None and len(b_arr) >= 4:
        i = 2
        if len(b_arr) == b_arr[1] + 2:
            while i < len(b_arr):
                i2 = i + 1
                i3 = b_arr[i]
                i += 2
                i4 = b_arr[i2]
                if i4 > 0:
                    b_arr2 = b_arr[i : i + i4]
                    i += i4
                else:
                    b_arr2 = None
                data_bean = DataBean.get_data_bean(i3, b_arr2)
                if data_bean is not None and data_bean not in array_list:
                    array_list.append(data_bean)
    return array_list


def parse_earbud_setting(data):
    # \xff\x14\x06\x01\x01\x08\x03??\x7f\t\x01\x02\x0c\x01\x02\x10\x01\x00\x16\x012
    # first byte ignored
    # second byte is length
    # first byte of chunk is identifier
    # second byte of chunk is length
    # rest of chunk is data
    # \x06\x01\x01
    # \x08\x03??\x7f
    # \t\x01\x02
    # \x0c\x01\x02
    return process_byte_array(data)


"""
normal mode
b"\xff\x14\x06\x01\x01\x08\x03??\x7f\t\x01\x02\x0c\x01\x02\x10\x01\x00\x16\x012"
{'command': <CommandsEnum.RUER: 6>, 'data': b'\x01'}
{'command': <CommandsEnum.VOICE: 8>, 'data': b'??\x7f'}
{'command': <CommandsEnum.DIYANSHI: 9>, 'data': b'\x02'}
{'command': <CommandsEnum.NOISEMODE: 12>, 'data': b'\x02'}  <-- normal mode == \x02
{'command': <CommandsEnum.SLEEPMODE: 16>, 'data': b'\x00'}
{'command': <CommandsEnum.BALANCE: 22>, 'data': b'2'}

anc mode
b"\xff\x14\x06\x01\x01\x08\x03FF\x7f\t\x01\x02\x0c\x01c\x10\x01\x00\x16\x012"
{'command': <CommandsEnum.RUER: 6>, 'data': b'\x01'}
{'command': <CommandsEnum.VOICE: 8>, 'data': b'FF\x7f'}
{'command': <CommandsEnum.DIYANSHI: 9>, 'data': b'\x02'}
{'command': <CommandsEnum.NOISEMODE: 12>, 'data': b'c'} <-- anc mode == \x63
{'command': <CommandsEnum.SLEEPMODE: 16>, 'data': b'\x00'}
{'command': <CommandsEnum.BALANCE: 22>, 'data': b'2'}

passthrough mode
b"\xff\x14\x06\x01\x01\x08\x03FF\x7f\t\x01\x02\x0c\x01\xa5\x10\x01\x00\x16\x012"
{'command': <CommandsEnum.RUER: 6>, 'data': b'\x01'}
{'command': <CommandsEnum.VOICE: 8>, 'data': b'FF\x7f'}
{'command': <CommandsEnum.DIYANSHI: 9>, 'data': b'\x02'}
{'command': <CommandsEnum.NOISEMODE: 12>, 'data': b'\xa5'} <-- passthrough mode == \xa5
{'command': <CommandsEnum.SLEEPMODE: 16>, 'data': b'\x00'}
{'command': <CommandsEnum.BALANCE: 22>, 'data': b'2'}
"""


async def main(address):
    logger.info(f"Connecting to device: {address}")

    """
    logger.info(
        parse_earbud_setting(
            b"\xff\x14\x06\x01\x01\x08\x03FF\x7f\t\x01\x02\x0c\x01\xa5\x10\x01\x00\x16\x012"
        )
    )
    """

    async with BleakClient(address) as client:
        if client.is_connected:
            logger.info(f"Connected: {client}")

        # await explore_services(client)
        # logger.info(await battery_level(client))
        # logger.info(await get_firmware_version(client))


asyncio.run(main(DEVICE_ADDRESS))
