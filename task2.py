from PinDefinitions import button_led_pin, green_led_pin, orange_led_pin, red_led_pin


def light_led_by_id(leds, led_on_index):
    for i in range(len(leds)):
        leds[i].value(1 if led_on_index == i else 0)

def run():
    leds = [green_led_pin, orange_led_pin, red_led_pin]
    led_on_index = 0

    light_led_by_id(leds, led_on_index)

    was_button_pressed = False
    while True:
        isButtonPressed = button_led_pin.value()
        if isButtonPressed and not was_button_pressed:
            led_on_index = (led_on_index + 1) % 3
            light_led_by_id(leds, led_on_index)

        was_button_pressed = isButtonPressed
