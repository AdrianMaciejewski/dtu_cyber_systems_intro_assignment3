from machine import I2C

from Task import Task
from PinDefinitions import green_led_pin, orange_led_pin, red_led_pin, sda_pin, scl_pin, i2c


def convert_to_celcius(data):
    value = (data[0] << 8) | data[1]
    temp = (value & 0xFFF) / 16
    if value & 0x1000:
        temp -= 256
    return temp

def read_temperature(i2c):
    data = bytearray(2)
    i2c.readfrom_mem_into(24,5,data)
    temp = convert_to_celcius(data)
    return temp

class Task3(Task):
    def __init__(self):
        self.i2c = i2c
        self.GREEN_ORANGE_THRESHOLD = 28
        self.ORANGE_RED_THRESHOLD = 31

    def run_iteration(self):
        temp = read_temperature(self.i2c)

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
