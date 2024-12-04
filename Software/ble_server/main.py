from bluetooth import *
import requests

import asyncio
cubby = BLE_UART(peripheral_name='CubbySense', address = 'D381E5F7-AFC1-E128-7309-5C87C3123971')

host_ip = "192.168.0.164"
host_port = "8081"

async def update_leds():
  await cubby.connect()
  while True:
    if (cubby.isConnected):
      response = requests.get(f"http://{host_ip}:{host_port}/leds")
      await asyncio.sleep(0.5) # To not spam server
      if response.status_code == 200:  # HTTP 200 means OK
        print("Get request successful")
        leds_data = response.json()
        sorted_leds = sorted(leds_data["leds"], key=lambda led: led["id"]) # Sort the data by the ID number
        if (sorted_leds[0]["color"] == "on"): # Index zero is the update check (should be ON if it just got updated)
          print("Was just updated!") 
          message = ""
          for led in sorted_leds[1:]:
            led_msg_body = {
              "color": "off",
              "id": -1
            }
            response = requests.put(url=f"http://{host_ip}:{host_port}/leds/-1", json=led_msg_body) # Reset the update check
            
            
            if led["color"] == "off":
              message += "0"
            if led["color"] == "on":
              message += "1"
            if led["color"] == "new":
              message += "2"
          print(f"Formatted LED message: {message}")
          
          await cubby.write(message)
          
          await asyncio.sleep(10)
          
          await cubby.write("0000") # Turn the leds off after 5 seconds
            
            
      else:
        print(f"Request failed with status code: {response.status_code}")
    else:
      await cubby.connect()

asyncio.run(update_leds())
