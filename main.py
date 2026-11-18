
import network
import urequests
import time
import json
from machine import Pin, ADC
import dht


# WIFI CONFIGURATION
SSID = "YOUR_WIFI_NAME"
PASSWORD = "YOUR_WIFI_PASSWORD"

SERVER_IP = "192.168.100.115"
API_URL = "http://{}/add.php".format(SERVER_IP)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# SENSOR CONFIGURATION
# DHT22 - GP2
sensor = dht.DHT22(Pin(2))

# Soil Moisture - GP26
soil = ADC(26)

# LDR - GP14
ldr = Pin(14, Pin.IN)


def connect_wifi():

    if wlan.isconnected():
        return True

    print("[WIFI] Connecting...")

    try:
        wlan.connect(SSID, PASSWORD)

        for _ in range(15):

            if wlan.isconnected():
                print("[WIFI] Connected!")
                print("[WIFI] IP Address:", wlan.ifconfig()[0])
                return True

            time.sleep(1)

    except Exception as e:
        print("[WIFI ERROR]", e)

    print("[WIFI] Connection failed.")
    return False


def read_soil():

    raw_value = soil.read_u16()

    moisture = int(
        100 - (raw_value / 65535 * 100)
    )

    return max(0, min(100, moisture))


def read_light():

    return "MALIWANAG" if ldr.value() == 0 else "MADILIM"


def read_dht():

    try:
        sensor.measure()

        temp = sensor.temperature()
        hum = sensor.humidity()

        return temp, hum

    except Exception as e:

        print("[DHT ERROR]", e)
        return None, None


def send_data():

    temp, hum = read_dht()

    if temp is None or hum is None:
        print("[ERROR] Unable to read DHT22.")
        return

    soil_val = read_soil()
    light = read_light()

    data = {
        "temperature": temp,
        "humidity": hum,
        "soil_moisture": soil_val,
        "light_status": light
    }

    print("\n==============================")
    print("SMART PLANT SENSOR RESULTS")
    print("==============================")

    print("Temperature :", temp, "°C")
    print("Humidity    :", hum, "%")
    print("Soil        :", soil_val, "%")
    print("Light       :", light)

    print("==============================")

    try:

        response = urequests.post(
            API_URL,
            data=json.dumps(data),
            headers={
                "Content-Type": "application/json"
            }
        )

        print("[SERVER RESPONSE]", response.text)
        response.close()

    except Exception as e:

        print("[HTTP ERROR]", e)


print("[SYSTEM] SMART PLANT SYSTEM STARTING")

connect_wifi()

while True:

    try:

        if wlan.isconnected():
            send_data()

        else:
            print("[WIFI] Disconnected. Reconnecting...")
            connect_wifi()

        time.sleep(2)

    except Exception as e:

        print("[SYSTEM ERROR]", e)
        time.sleep(2)
