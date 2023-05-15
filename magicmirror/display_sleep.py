'''
'''
import subprocess
import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM) 
Infrared_Sensor = 4
LED = 27
GPIO.setup(LED, GPIO.OUT)
GPIO.setup(Infrared_Sensor, GPIO.IN)

if __name__ == '__main__':
    try:
        while True:
            if GPIO.input(Infrared_Sensor) == 1:
                GPIO.output(LED,GPIO.HIGH)
                time.sleep(3)
            elif GPIO.input(Infrared_Sensor) == 0:
                time.sleep(3)
                if GPIO.input(Infrared_Sensor) == 0:
                    GPIO.output(LED,GPIO.LOW)
         
    except KeyboardInterrupt:
        GPIO.cleanup()