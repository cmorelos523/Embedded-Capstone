import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
while True:
    if GPIO.input(17) == GPIO.HIGH:
        time.sleep(1) #Sleep for one sec
    if GPIO.input(17) == GPIO.HIGH:
        print("You have been pressing the button for 1 sec!")