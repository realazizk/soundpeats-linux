import asyncio  
from bleak import BleakClient  
import binascii  
import logging  
from dbus_next.aio import MessageBus  
from dbus_next.service import ServiceInterface, method, dbus_property, signal  
from dbus_next import Variant
  
DEVICE_ADDRESS = "C4:AC:60:E0:75:95"  
  
logging.basicConfig(level=logging.INFO)  
logger = logging.getLogger(__name__)  
  
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
        if self.client:  
            await self.client.disconnect()  
            logger.info("Disconnected")  
  
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
                        value = await self.client.read_gatt_descriptor(descriptor.handle)  
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
  
    @method()  
    async def GetBatteryLevel(self) -> 'a{sv}':  
        battery = await self.battery_level()  
        return {'left': Variant('y', battery['left']), 'right': Variant('y', battery['right'])}  
  
    @method()  
    async def Connect(self) -> 's':  
        await self.connect(DEVICE_ADDRESS)  
        return "Connected"  
  
    @method()  
    async def Disconnect(self) -> 's':  
        await self.disconnect()  
        return "Disconnected"  
  
    @method()  
    async def ExploreServices(self) -> 's':  
        await self.explore_services()  
        return "Services Explored"  
  
async def main():  
    bus = await MessageBus().connect()  
    service = BLEService('tn.aziz.soundpeats.BLEService')  
    bus.export('/tn/aziz/soundpeats/BLEService', service)  
    await bus.request_name('tn.aziz.soundpeats.BLEService')
    logger.info("D-Bus service started")  
    await asyncio.Future()
  
if __name__ == "__main__":  
    asyncio.run(main())  
