from machine import I2C

from PinDefinitions import green_led_pin, orange_led_pin, red_led_pin, sda_pin, scl_pin


def convert_to_celcius(data):
    value = (data[0] << 8) | data[1]
    temp = (value & 0xFFF) / 16
    if value & 0x1000:
        temp -= 256
    return temp


def run():
    i2c = I2C(scl=scl_pin,sda=sda_pin)
    
    print(i2c.scan())

    data = bytearray(2)
    while True:
        i2c.readfrom_mem_into(24,5,data)
        temp = convert_to_celcius(data)
        
        green_led_pin.value(0)
        orange_led_pin.value(0)
        red_led_pin.value(0)

        green_orange_threshold = 28
        orange_red_threshold = 31
        
        if temp < green_orange_threshold:
            green_led_pin.value(1)
            orange_led_pin.value(0)
            red_led_pin.value(0)
        elif temp >= green_orange_threshold and temp <= orange_red_threshold:
            green_led_pin.value(0)
            orange_led_pin.value(1)
            red_led_pin.value(0)
        elif temp > orange_red_threshold:
            green_led_pin.value(0)
            orange_led_pin.value(0)
            red_led_pin.value(1)

        print(temp)
