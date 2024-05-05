from machine import ADC, PWM

from Task import Task
from PinDefinitions import potentiometer_pin, rgb_led_red_pin, rgb_led_green_pin, rgb_led_blue_pin, red_pwm, green_pwm, blue_pwm, potentiometer_adc
from Utils import get_potentiometer_load, MIN_POTENTIOMETER_VOLTAGE, MAX_POTENTIOMETER_VOLTAGE, MAX_DUTY

class Task5(Task):
    def __init__(self):
        self.red_pwm = red_pwm
        self.green_pwm = green_pwm
        self.blue_pwm = blue_pwm

    def run_iteration(self):
        voltage_load = get_potentiometer_load()

        duty=int(MAX_DUTY*voltage_load)
        self.red_pwm.duty(duty)
        self.green_pwm.duty(duty)
        self.blue_pwm.duty(duty)

        print(f"Task5; voltage load: {voltage_load}")

    def end_task(self):
        duty=0
        self.red_pwm.duty(duty)
        self.green_pwm.duty(duty)
        self.blue_pwm.duty(duty)
