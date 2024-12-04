import requests

host_ip = "192.168.0.164"
host_port = "8081"

led_msg_body = {
    "color": "off",
    "id": -1
}
response = requests.put(url=f"http://{host_ip}:{host_port}/leds/-1", json=led_msg_body)
# Check and handle the response
if response.status_code == 200:
    print("Success:", response.json())
elif response.status_code == 404:
    print("Not Found:", response.json())
else:
    print("Error:", response.status_code, response.text)
