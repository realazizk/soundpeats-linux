import asyncio
import enum
from typing import Any, Dict, List, Optional
from bleak import BleakClient
import binascii
import logging
from dbus_next.aio import MessageBus
from dbus_next.service import ServiceInterface, method
from dbus_next import Variant

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


class NoiseMode(enum.IntEnum):
    NORMAL = 0x02
    ANC = 0x63
    PASSTHROUGH = 0xA5


async def get_service(client: BleakClient):
    global SERVICE
    if SERVICE:
        return SERVICE
    service_uuid = "0000a001-0000-1000-8000-00805f9b34fb"
    (SERVICE,) = (s for s in client.services if s.uuid == service_uuid)
    return SERVICE


def pack_data_to_send(*bArr):
    # Initialize a bytearray of size 256
    bArr2 = bytearray(256)
    i = 2
    # Concatenate the input byte arrays into bArr2
    for bArr3 in bArr:
        bArr2[i : i + len(bArr3)] = bArr3
        i += len(bArr3)
    # Create the final byte array of the correct size
    bArr4 = bytearray(i)
    bArr4[0] = 0xFF
    bArr4[1] = i - 2
    bArr4[2:] = bArr2[2:i]
    return bytes(bArr4)


async def set_noise_mode(client: BleakClient, mode: NoiseMode):
    uuid = "00001001-0000-1000-8000-00805f9b34fb"
    service = await get_service(client)
    char = service.get_characteristic(uuid)
    if not char:
        logger.error("Characteristic not found")
        return
    await client.write_gatt_char(
        char,
        pack_data_to_send(bytes([12, 1, mode.value])),
    )


DataBeanType = Dict[str, Any]


def get_data_bean(i: int, b_arr: Optional[bytearray]) -> DataBeanType:
    return {
        "command": CommandsEnum(i),
        "data": b_arr,
    }


def process_byte_array(b_arr) -> List[DataBeanType]:
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
                data_bean = get_data_bean(i3, b_arr2)
                if data_bean is not None and data_bean not in array_list:
                    array_list.append(data_bean)
    return array_list


def parse_earbud_setting(data):
    return process_byte_array(data)


class BLEService(ServiceInterface):
    def __init__(self, bus_name):
        super().__init__(bus_name)
        self.client = None

    async def connect(self, address):
        logger.info(f"Connecting to device: {address}")
        self.client = BleakClient(address)
        await self.client.connect()
        if self.client.is_connected:
            logger.info(f"Connected: {self.client}")

    async def disconnect(self):
        q

    async def explore_services(self):
        if not self.client:
            raise Exception("Not connected to any device")
        for service in self.client.services:
            logger.info("[Service] %s", service)
            for char in service.characteristics:
                if "read" in char.properties:
                    try:
                        value = await self.client.read_gatt_char(char.uuid)
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
                        value = await self.client.read_gatt_descriptor(
                            descriptor.handle
                        )
                        logger.info("    [Descriptor] %s, Value: %r", descriptor, value)
                    except Exception as e:
                        logger.error("    [Descriptor] %s, Error: %s", descriptor, e)

    async def battery_level(self):
        if not self.client:
            raise Exception("Not connected to any device")
        uuid = "00000008-0000-1000-8000-00805f9b34fb"
        out = await self.client.read_gatt_char(uuid)
        logger.info(f"Received: {out}, {binascii.hexlify(out)}")
        return {
            "left": out[0],
            "right": out[1],
        }

    async def get_firmware_version(self):
        if not self.client:
            raise Exception("Not connected to any device")
        uuid = "00000007-0000-1000-8000-00805f9b34fb"
        service = await get_service(self.client)
        char = service.get_characteristic(uuid)
        if not char:
            logger.error("Characteristic not found")
            return
        out = await self.client.read_gatt_char(char)
        logger.info(f"Received: {out}, {binascii.hexlify(out)}")
        return out.decode()

    async def read_earbud_setting(self):
        if not self.client:
            raise Exception("Not connected to any device")
        uuid = "00001002-0000-1000-8000-00805f9b34fb"
        service = await get_service(self.client)
        char = service.get_characteristic(uuid)
        if not char:
            logger.error("Characteristic not found")
            raise Exception("Characteristic not found")

        out = await self.client.read_gatt_char(char)
        logger.info(f"Received: {out}, {binascii.hexlify(out)}")
        return parse_earbud_setting(out)

    @method()
    async def GetBatteryLevel(self) -> "a{sv}":
        battery = await self.battery_level()
        return {
            "left": Variant("y", battery["left"]),
            "right": Variant("y", battery["right"]),
        }

    @method()
    async def Connect(self, address: "s") -> "s":
        await self.connect(address)
        return "Connected"

    @method()
    async def Disconnect(self) -> "s":
        await self.disconnect()
        return "Disconnected"

    @method()
    async def ExploreServices(self) -> "s":
        await self.explore_services()
        return "Services Explored"

    @method()
    async def GetFirmwareVersion(self) -> "s":
        version = await self.get_firmware_version()
        return version

    @method()
    async def GetEarbudSettings(self) -> "a{sv}":
        settings = await self.read_earbud_setting()
        return {
            str(i): Variant(
                "a{sv}",
                {
                    "command": Variant("s", setting["command"].name),
                    "data": (
                        Variant("ay", bytes(setting["data"]))
                        if setting["data"] is not None
                        else Variant("ay", b"")
                    ),
                },
            )
            for i, setting in enumerate(settings)
        }

    @method()
    async def SetNoiseMode(self, mode: "s") -> "s":
        if not self.client:
            raise Exception("Not connected to any device")
        try:
            noise_mode = NoiseMode[mode.upper()]
        except KeyError:
            raise ValueError(f"Invalid noise mode: {mode}")
        await set_noise_mode(self.client, noise_mode)
        return f"Noise mode set to {mode}"


async def main():
    bus = await MessageBus().connect()
    service = BLEService("tn.aziz.soundpeats.BLEService")
    bus.export("/tn/aziz/soundpeats/BLEService", service)
    await bus.request_name("tn.aziz.soundpeats.BLEService")
    logger.info("D-Bus service started")
    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
