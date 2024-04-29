from machine import Pin, PWM, I2C

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

red_pwm = PWM(Pin(IO15, Pin.OUT), duty=0)
green_pwm = PWM(Pin(IO32, Pin.OUT), duty=0)
blue_pwm = PWM(Pin(IO14, Pin.OUT), duty=0)

SDA=23
sda_pin = Pin(SDA, Pin.OUT)
SCL=22
scl_pin = Pin(SCL, Pin.OUT)
i2c = I2C(scl=scl_pin,sda=sda_pin)

A5=4
potentiometer_pin = Pin(A5, Pin.IN)

A4=36
button_change_task = Pin(A4, Pin.IN)


pins = [
            {'id': IO13, 'name': 'Button led pin', 'type': 1, 'pin': button_led_pin, 'pwm': None},
            {'id': IO12, 'name': 'Green led pin', 'type': 1, 'pin': green_led_pin, 'pwm': None},
            {'id': IO27, 'name': 'Orange led pin', 'type': 1, 'pin': orange_led_pin, 'pwm': None},
            {'id': IO33, 'name': 'Red led pin', 'type': 1, 'pin': red_led_pin, 'pwm': None},
            {'id': IO15, 'name': 'RGB led red pin', 'type': 2, 'pin': rgb_led_red_pin, 'pwm': red_pwm},
            {'id': IO32, 'name': 'RGB led green pin', 'type': 2, 'pin': rgb_led_green_pin, 'pwm': green_pwm},
            {'id': IO14, 'name': 'RGB led blue pin', 'type': 2, 'pin': rgb_led_blue_pin, 'pwm': blue_pwm},
            {'id': SDA, 'name': 'SDA pin', 'type': 1, 'pin': sda_pin, 'pwm': None},
            {'id': SCL, 'name': 'SCL pin', 'type': 1, 'pin': scl_pin, 'pwm': None},
            {'id': A5, 'name': 'Potentiometer pin', 'type': 1, 'pin': potentiometer_pin, 'pwm': None},
            {'id': A4, 'name': 'Button change task', 'type': 1, 'pin': button_change_task, 'pwm': None},
        ]