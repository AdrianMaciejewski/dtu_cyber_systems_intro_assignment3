from Task import Task
from PinDefinitions import button_led_pin, green_led_pin, orange_led_pin, red_led_pin


class Task2(Task):
    def __init__(self):
        self.leds = [green_led_pin, orange_led_pin, red_led_pin]
        self.led_on_index = 0
        self.was_button_pressed = False

    def _light_led_by_id(self):
        for i in range(len(self.leds)):
            self.leds[i].value(1 if self.led_on_index == i else 0)

    def run_iteration(self):
        isButtonPressed = button_led_pin.value()
        if isButtonPressed and not self.was_button_pressed:
            self.led_on_index = (self.led_on_index + 1) % 3
            self._light_led_by_id()
        self.was_button_pressed = isButtonPressed

    def start_task(self):
        self.led_on_index = 0
        self.was_button_pressed = False

        self._light_led_by_id()
    
    def end_task(self):
        green_led_pin.value(0)
        orange_led_pin.value(0)
        red_led_pin.value(0)
