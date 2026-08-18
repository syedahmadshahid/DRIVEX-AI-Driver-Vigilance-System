import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

BUZZER = 18

GPIO.setup(BUZZER, GPIO.OUT)

last_alert_time = 0

def buzz(duration):

    GPIO.output(BUZZER, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(BUZZER, GPIO.LOW)

def play_warning():

    global last_alert_time

    if time.time() - last_alert_time > 1:

        buzz(0.2)

        print("WARNING ALERT")

        last_alert_time = time.time()

def play_critical():

    global last_alert_time

    if time.time() - last_alert_time > 1:

        buzz(0.7)

        print("CRITICAL ALERT")

        last_alert_time = time.time()