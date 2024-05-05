from machine import Pin, PWM, I2C, ADC

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

A3=39 # do not use ADC2 pin beause ADC2 is used by WIFI module https://stackoverflow.com/questions/77635257/micropython-wifi-and-adc-sensor-not-working-together
potentiometer_pin = Pin(A3, Pin.IN)
potentiometer_adc = ADC(potentiometer_pin)

A4=36
button_change_task = Pin(A4, Pin.IN)


pins = [
            {'id': 1, 'pinNumber': IO13, 'isReadOnly': True, 'name': 'Button led pin', 'type': 1, 'pin': button_led_pin, 'pwm': None, 'adc': None},
            {'id': 2, 'pinNumber': IO12, 'isReadOnly': False, 'name': 'Green led pin', 'type': 1, 'pin': green_led_pin, 'pwm': None, 'adc': None},
            {'id': 3, 'pinNumber': IO27, 'isReadOnly': False, 'name': 'Orange led pin', 'type': 1, 'pin': orange_led_pin, 'pwm': None, 'adc': None},
            {'id': 4, 'pinNumber': IO33, 'isReadOnly': False, 'name': 'Red led pin', 'type': 1, 'pin': red_led_pin, 'pwm': None, 'adc': None},
            {'id': 5, 'pinNumber': IO15, 'isReadOnly': False, 'name': 'RGB led red pin', 'type': 2, 'pin': rgb_led_red_pin, 'pwm': red_pwm, 'adc': None},
            {'id': 6, 'pinNumber': IO32, 'isReadOnly': False, 'name': 'RGB led green pin', 'type': 2, 'pin': rgb_led_green_pin, 'pwm': green_pwm, 'adc': None},
            {'id': 7, 'pinNumber': IO14, 'isReadOnly': False, 'name': 'RGB led blue pin', 'type': 2, 'pin': rgb_led_blue_pin, 'pwm': blue_pwm, 'adc': None},
            {'id': 8, 'pinNumber': SDA, 'isReadOnly': True, 'name': 'SDA pin', 'type': 1, 'pin': sda_pin, 'pwm': None, 'adc': None},
            {'id': 9, 'pinNumber': SCL, 'isReadOnly': True, 'name': 'SCL pin', 'type': 1, 'pin': scl_pin, 'pwm': None, 'adc': None},
            {'id': 10, 'pinNumber': A3, 'isReadOnly': True, 'name': 'Potentiometer pin', 'type': 3, 'pin': potentiometer_pin, 'pwm': None, 'adc': potentiometer_adc},
            {'id': 11, 'pinNumber': A4, 'isReadOnly': True, 'name': 'Button change task', 'type': 1, 'pin': button_change_task, 'pwm': None, 'adc': None},
        ]