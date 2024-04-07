import time

from Task import Task
from PinDefinitions import button_led_pin, red_led_pin

class Task1(Task):
    def run_iteration(self):
        isButtonPressed = button_led_pin.value()

        if isButtonPressed:
            time.sleep(0.5)
            red_led_pin.value(not red_led_pin.value())
        else:
            red_led_pin.value(0)
