from machine import Pin

IO13=13
button_led_pin = Pin(IO13, Pin.OUT)
IO12=12
green_led_pin = Pin(IO12, Pin.OUT)
IO27=27
orange_led_pin = Pin(IO27, Pin.OUT)
IO33=33
red_led_pin = Pin(IO33, Pin.OUT)

IO15=15
rgb_led_red_pin = Pin(IO15, Pin.OUT)
IO32=32
rgb_led_green_pin = Pin(IO32, Pin.OUT)
IO14=14
rgb_led_blue_pin = Pin(IO14, Pin.OUT)

SDA=23
sda_pin = Pin(SDA, Pin.OUT)
SCL=22
scl_pin = Pin(SCL, Pin.OUT)

A5=4
potentiometer_pin = Pin(A5, Pin.IN)