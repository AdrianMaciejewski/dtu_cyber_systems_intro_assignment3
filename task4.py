from machine import I2C

from PinDefinitions import rgb_led_red_pin, rgb_led_green_pin, rgb_led_blue_pin, sda_pin, scl_pin
from task3 import convert_to_celcius


def run():
    i2c = I2C(scl=scl_pin,sda=sda_pin)
    
    print(i2c.scan())

    data = bytearray(2)
    while True:
        i2c.readfrom_mem_into(24,5,data)
        temp = convert_to_celcius(data)

        green_orange_threshold = 28
        orange_red_threshold = 31
        
        if temp < green_orange_threshold:
            rgb_led_red_pin.value(0)
            rgb_led_green_pin.value(1)
            rgb_led_blue_pin.value(0)
        elif temp >= green_orange_threshold and temp <= orange_red_threshold:
            rgb_led_red_pin.value(1)
            rgb_led_green_pin.value(1)
            rgb_led_blue_pin.value(0)
        elif temp > orange_red_threshold:
            rgb_led_red_pin.value(1)
            rgb_led_green_pin.value(0)
            rgb_led_blue_pin.value(0)

        print(temp)
