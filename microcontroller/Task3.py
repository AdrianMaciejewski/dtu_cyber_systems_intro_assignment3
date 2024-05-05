from machine import I2C

from Task import Task
from PinDefinitions import green_led_pin, orange_led_pin, red_led_pin, sda_pin, scl_pin, i2c
from Utils import read_temperature

class Task3(Task):
    def __init__(self):
        self.GREEN_ORANGE_THRESHOLD = 28
        self.ORANGE_RED_THRESHOLD = 31

    def run_iteration(self):
        temp = read_temperature()

        if temp < self.GREEN_ORANGE_THRESHOLD:
            green_led_pin.value(1)
            orange_led_pin.value(0)
            red_led_pin.value(0)
        elif temp >= self.GREEN_ORANGE_THRESHOLD and temp <= self.ORANGE_RED_THRESHOLD:
            green_led_pin.value(0)
            orange_led_pin.value(1)
            red_led_pin.value(0)
        elif temp > self.ORANGE_RED_THRESHOLD:
            green_led_pin.value(0)
            orange_led_pin.value(0)
            red_led_pin.value(1)
        
        print(f"Task3; Temperature: {temp}")
    
    def end_task(self):
        green_led_pin.value(0)
        orange_led_pin.value(0)
        red_led_pin.value(0)
