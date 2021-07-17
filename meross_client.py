import asyncio
import os

from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager

EMAIL = os.environ.get('MEROSS_EMAIL') 
PASSWORD = os.environ.get('MEROSS_PASSWORD') 


async def onOff():
    # Setup the HTTP client API from user-password
    http_api_client = await MerossHttpClient.async_from_user_password(email=EMAIL, password=PASSWORD)

    # Setup and start the device manager
    manager = MerossManager(http_client=http_api_client)
    await manager.async_init()

    # Retrieve all the devices that implement the electricity mixin
    await manager.async_device_discovery()
    devs = manager.find_devices(device_type="mss210")

    if len(devs) < 1:
        print("No plugs found.")
    else:
        
        for dev in devs:
            if (dev.name == "office radiator"):
                await dev.async_update()
                print(f"dev name: {dev.name}")
                await dev.async_update()
                await dev.async_turn_on(channel=0)
                await asyncio.sleep(5)
                await dev.async_turn_off(channel=0)

    # Close the manager and logout from http_api
    manager.close()
    await http_api_client.async_logout()

if __name__ == '__main__':
    # On Windows + Python 3.8, you should uncomment the following
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(onOff())
    loop.close()
