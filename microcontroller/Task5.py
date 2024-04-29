from machine import ADC, PWM

from Task import Task
from PinDefinitions import potentiometer_pin, rgb_led_red_pin, rgb_led_green_pin, rgb_led_blue_pin, red_pwm, green_pwm, blue_pwm


class Task5(Task):
    def __init__(self):
        self.MIN_VOLTAGE = 63*1000
        self.MAX_VOLTAGE = 1048*1000
        self.MAX_DUTY = 2**10-1

        self.red_pwm = red_pwm
        self.green_pwm = green_pwm
        self.blue_pwm = blue_pwm

        self.adc = ADC(potentiometer_pin)

    def run_iteration(self):
        voltage = self.adc.read_uv()
        voltage_load = (voltage - self.MIN_VOLTAGE) / (self.MAX_VOLTAGE - self.MIN_VOLTAGE) # value from 0 to 1
        voltage_load = min(abs(voltage_load),1) # just make sure that it is within the range

        duty=int(self.MAX_DUTY*voltage_load)
        self.red_pwm.duty(duty)
        self.green_pwm.duty(duty)
        self.blue_pwm.duty(duty)

        print(f"Task5; voltage load: {voltage_load}")

    def end_task(self):
        duty=0
        self.red_pwm.duty(duty)
        self.green_pwm.duty(duty)
        self.blue_pwm.duty(duty)
