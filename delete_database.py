import requests

host_ip = "192.168.0.141"
host_port = "8081"

for i in range(0,4):
  response = requests.delete(url=f"http://{host_ip}:{host_port}/items/cubby/{i}")
  # Check and handle the response
  if response.status_code == 200:
      print("Success:", response.json())
  elif response.status_code == 404:
      print("Not Found:", response.json())
  else:
      print("Error:", response.status_code, response.text)
