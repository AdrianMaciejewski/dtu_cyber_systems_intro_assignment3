from machine import ADC, PWM

from PinDefinitions import potentiometer_pin, rgb_led_red_pin, rgb_led_green_pin, rgb_led_blue_pin


def run():
    MIN_VOLTAGE = 63*1000
    MAX_VOLTAGE = 1048*1000

    MAX_DUTY = 2**10-1

    red_pwm = PWM(rgb_led_red_pin, duty=0)
    green_pwm = PWM(rgb_led_green_pin, duty=0)
    blue_pwm = PWM(rgb_led_blue_pin, duty=0)

    while True:
        adc = ADC(potentiometer_pin)
        voltage = adc.read_uv()
        voltage_load = (voltage - MIN_VOLTAGE) / (MAX_VOLTAGE - MIN_VOLTAGE) # value from 0 to 1
        voltage_load = min(abs(voltage_load),1) # just make sure that it is within the range

        duty=int(MAX_DUTY*voltage_load)
        red_pwm.duty(duty)
        green_pwm.duty(duty)
        blue_pwm.duty(duty)

        print(voltage_load)
