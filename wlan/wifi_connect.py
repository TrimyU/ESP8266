#你需要在程序根目录创建一个"wifi.json"文件.
from machine import Pin
import network
import time
import json

print("\n")


wlan = network.WLAN(network.STA_IF)
led = Pin(2, Pin.OUT)


def listToDict(n, m):
    op = {n[i]: m[i] for i in range(0, len(n))}
    return op


def wifi_connect(name, password):
    wifi_led = Pin(2, Pin.OUT)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    start_time = time.time()

    if not wlan.isconnected():
        print(
            "Currently wireless is not connected to the Internet, it is connecting...."
        )
        wlan.connect(name, password)
        while not wlan.isconnected():
            wifi_led.value(0)
            time.sleep_ms(700)
            wifi_led.value(1)
            time.sleep_ms(700)
            print("Trying to connect to wifi....")
            print(time.time())

            if time.time() - start_time > 16:
                print("Unable to connect to the network.")
                break

    if wlan.isconnected():
        wifi_led.value(0)
        IP_info = wlan.ifconfig()
        print("The wireless network is connected and the information is as follows:")
        print("SSID:" + name)
        print("IP:" + IP_info[0])
        print("Subnet mask:" + IP_info[1])
        print("Gateway:" + IP_info[2])
        print("DNS:" + IP_info[3])
        return True


with open("wifi.json") as f:
    wifi = json.load(f)
names = wifi["name"].split(";")
password = wifi["password"].split(";")

led.value(0)
wifi_list = wlan.scan()
led.value(1)
time.sleep_ms(500)

wifi_local = listToDict(names, password)

for i in range(len(wifi_list)):
    if str(wifi_list[i][0])[2:-1] in names:
        wifi_connect(str(wifi_list[i][0])[2:-1], wifi_local[str(wifi_list[i][0])[2:-1]])
        break

import webrepl
webrepl.start()
