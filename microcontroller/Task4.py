from machine import I2C, PWM

from PinDefinitions import rgb_led_red_pin, rgb_led_green_pin, rgb_led_blue_pin, sda_pin, scl_pin, red_pwm, green_pwm, blue_pwm
from Task3 import Task3
from Utils import MAX_DUTY, read_temperature


class Task4(Task3):
    def __init__(self):
        super().__init__()
        self.red_pwm = red_pwm
        self.green_pwm = green_pwm
        self.blue_pwm = blue_pwm

    def run_iteration(self):
        temp = read_temperature()
        
        if temp < self.GREEN_ORANGE_THRESHOLD:
            self.red_pwm.duty(0)
            self.green_pwm.duty(MAX_DUTY)
            self.blue_pwm.duty(0)
        elif temp >= self.GREEN_ORANGE_THRESHOLD and temp <= self.ORANGE_RED_THRESHOLD:
            self.red_pwm.duty(MAX_DUTY)
            self.green_pwm.duty(MAX_DUTY)
            self.blue_pwm.duty(0)
        elif temp > self.ORANGE_RED_THRESHOLD:
            self.red_pwm.duty(MAX_DUTY)
            self.green_pwm.duty(0)
            self.blue_pwm.duty(0)

        print(f"Task4; Temperature: {temp}")
    
    def end_task(self):
        self.red_pwm.duty(0)
        self.green_pwm.duty(0)
        self.blue_pwm.duty(0)