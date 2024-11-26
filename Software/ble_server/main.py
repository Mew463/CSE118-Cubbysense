from bluetooth import *
import requests

import asyncio
cubby = BLE_UART(peripheral_name='CubbySense', address = 'D381E5F7-AFC1-E128-7309-5C87C3123971')

host_ip = "192.168.0.141"
host_port = "8081"

async def update_leds():
  await cubby.connect()
  while True:
    x = input("msg:")
    if (cubby.isConnected):
      response = requests.get("{host_ip}:{host_port}/leds")
      # Check the status of the response
      if response.status_code == 200:  # HTTP 200 means OK
          print("Success!")
          for led in response["leds"]:
            led[]
          
          
          print(response.text)  # The response content as a string
      else:
          print(f"Request failed with status code: {response.status_code}")
      
      asyncio.sleep(0.5)
      
      await cubby.write(x)
    else:  
      await cubby.connect()
  

asyncio.run(update_leds())
