
import requests

host_ip = "192.168.0.141"
host_port = "8081"

response = requests.get(f"http://{host_ip}:{host_port}/leds")
# Check the status of the response
if response.status_code == 200:  # HTTP 200 means OK
    print("Success!")
    # print(response.json())
    # for 
    leds_data = response.json()
    sorted_leds = sorted(leds_data["leds"], key=lambda led: led["id"])
    for eachCubby in sorted_leds:
      print(eachCubby['color'])
    # print(sorted_leds)

# async def update_leds():
#   await cubby.connect()
#   while True:
#     #x = input("msg:")
#     if (cubby.isConnected):
#       response = requests.get(f"http://{host_ip}:{host_port}/leds")
#       # Check the status of the response
#       if response.status_code == 200:  # HTTP 200 means OK
#           print("Success!")
#           leds_data = response.json()
#           sorted_leds = sorted(leds_data["leds"], key=lambda led: led["id"])
#           message = ""
#           for led in response["leds"]:
#             if led["color"] == "off":
#               message += "0"
#             if led["color"] == "on":
#               message += "1"
#             if led["color"] == "new":
#               message += "2"
#           print(f"Formatted LED message: {message}")
#       else:
#           print(f"Request failed with status code: {response.status_code}")

#       asyncio.sleep(0.5)

#       await cubby.write(message.encode())
#     else:
#       await cubby.connect()

# asyncio.run(update_leds())
