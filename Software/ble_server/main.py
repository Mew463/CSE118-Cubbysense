from bluetooth import *
import requests

import asyncio
cubby = BLE_UART(peripheral_name='CubbySense', address = 'D381E5F7-AFC1-E128-7309-5C87C3123971')
        
async def bluetooth_loop():
  await cubby.connect()
  while True:
    x = input("msg:")
    if (cubby.isConnected):
      await cubby.write(x)
    else:  
      await cubby.connect()
  
asyncio.run(bluetooth_loop())
