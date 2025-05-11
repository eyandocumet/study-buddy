# Runs on boot
# Tiffelyn Kurniawan

import network
import time
from umqtt.simple import MQTTClient
from machine import Pin, PWM

# Config, Init.
SSID_NAME = "ssid"
SSID_PASSWORD = "1234"
MQTT_BROKER = "smartnest.cz"
MQTT_PORT = 1883
MQTT_USERNAME = "user"
MQTT_PASSWORD = "pass"
MQTT_CLIENT = "big_number"
FIRMWARE_VERSION = "Timer-Notifier"
TIMER_DURATION_MIN = 0.1  # timer duration in minutes

# Setup button on GPIO13
button = Pin(12, Pin.IN, Pin.PULL_UP)  # HIGH when not pressed, LOW when pressed

# Connect to Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID_NAME, SSID_PASSWORD)
    while not wlan.isconnected():
        print("Connecting to WiFi...")
        time.sleep(1)
    print("WiFi Connected:", wlan.ifconfig())

# Send message to MQTT broker
def send_to_broker(sub_topic, message):
    full_topic = f"{MQTT_CLIENT}/{sub_topic}"
    client.publish(full_topic, message)
    print(f"Sent to {full_topic} → {message}")

# Timer end: notify + beep
def timer_done():
    print("Time's up! Sending notification and beeping...")
    send_to_broker("report/notification", "Break time!")

# Timer countdown
def start_timer():
    global buzzer
    buzzer = PWM(Pin(27))  # Re-initialize buzzer every time
    buzzer.duty(0)

    print(f"Timer started for {TIMER_DURATION_MIN} minutes")
    send_to_broker("report/timer", f"Started for {TIMER_DURATION_MIN} minutes")
    for i in range(int(TIMER_DURATION_MIN * 60), 0, -1):
        if i % 60 == 0 or i <= 10:
            print(f"   {i} seconds remaining...")
        time.sleep(1)
    timer_done()

# MAIN SETUP (Wi-Fi + MQTT connect once)
connect_wifi()

client = MQTTClient(client_id=MQTT_CLIENT,
                    server=MQTT_BROKER,
                    port=MQTT_PORT,
                    user=MQTT_USERNAME,
                    password=MQTT_PASSWORD)
client.connect()

send_to_broker("report/online", "true")
send_to_broker("report/firmware", FIRMWARE_VERSION)

# MAIN LOOP: wait for button press
print("Waiting for button press")
while True:
    if button.value() == 0:  # Button is pressed
        print("🔘 Button pressed! Running timer...")

        # Start countdown
        start_timer()

        # Debounce: wait for release
        while button.value() == 0:
            time.sleep(0.1)

        print("Finished. Waiting for next press.")

    time.sleep(0.1)
