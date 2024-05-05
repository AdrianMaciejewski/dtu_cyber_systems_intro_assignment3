import machine
import network
import socket
import uasyncio
import json

from PinDefinitions import button_led_pin, green_led_pin, orange_led_pin, red_led_pin, rgb_led_red_pin, rgb_led_green_pin, rgb_led_blue_pin, sda_pin, scl_pin, potentiometer_pin, button_change_task, red_pwm, green_pwm, blue_pwm, pins, i2c
from Utils import get_potentiometer_load, read_temperature, MAX_DUTY, getPinValue


"""
Handles the request by mapping it to a specific action that should be execited.
"""
class RequestHandler:
    def __init__(self):
        """
        Dictionary which is used as a mapping between a request and a method that should handle it. 
        Handling method is mapped by a specific path and request type.
        """
        self.endpoints = {'/': {'get': self._handleGetPinsView}, '/pins': {'get': self._handleGetPins}, '/sensors': {'get': self._handleGetSensors}, '/edit': {'get': self._handleEdit}}
    
    """
    Maps a request to its handler, if such is defined.
    """
    def handle_request(self, request_type, endpoint_path, params):
        response = "HTTP/1.1 404 Not found \r\n" + "Content-Type: text/html\r\n" +"\r\n" + "404 Not found"
        if endpoint_path.lower() in self.endpoints:
            if request_type.lower() in self.endpoints[endpoint_path]:
                response = self.endpoints[endpoint_path.lower()][request_type.lower()](**params)
        elif endpoint_path.lower().startswith('/edit'):
            if request_type.lower() in self.endpoints[endpoint_path]:
                response = self.endpoints['/edit'][request_type.lower()](**params)
        return response
    
    def _handleGetPinsView(self, **params):
        html = """
            <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body>
            <div class="body-container">
            <h1>ESP32 Pins</h1>
            <div class="table-container">
                <table>
                <thead>
                    <tr class="table100-head">
                    <th>Pin</th>
                    <th>Type</th>
                    <th>Value</th>
                    </tr>
                </thead>
                <tbody>
                    %s
                </tbody>
                </table>
            </div>
            </div>
        </body>
        %s
        </html>

        """
        update_script = """
        <script>
            async function updateValues() {
            try {
                const response = await fetch("http://192.168.4.1/pins");
                const data = await response.json();
                data.forEach((pin) => {
                const valueCell = document.getElementById(
                    `${pin.id.toString()}-value`
                );
                if (valueCell) {
                    if (valueCell) valueCell.textContent = pin.value;
                }
                });
            } catch (error) {
                console.error("Error fetching data:", error);
            }
            }

            // Schedule the function to fire every second
            setInterval(updateValues, 1000);
        </script>
        """
        style = """
        <style>
            * {
            box-sizing: border-box;
            padding: 0px;
            margin: 0px;
            }
            html {
            height: 100%;
            width: 100%;
            }
            body {
            display: flex;
            justify-content: center;
            height: 100%;
            width: 100%;
            background: linear-gradient(45deg, #4158d0, #c850c0);
            }
            h1 {
            height: 4rem;
            line-height: 4rem;
            text-align: center;
            color: #eee;
            }
            table {
            border: solid 0px black;
            border-radius: 1rem;
            overflow: hidden;
            border-spacing: 0;
            }
            thead {
            background: #36304a;
            }
            tbody {
            background: #e0e0e0;
            }
            th {
            padding: 0rem 2rem;
            text-align: left;
            font-family: OpenSans-Regular;
            font-size: 18px;
            color: #fff;
            line-height: 1.2;
            font-weight: unset;
            }
            th:first-child {
            padding: 0rem 1rem;
            }
            th:last-child {
            padding: 0rem 1rem;
            }
            tr {
            border: 0;
            height: 50px;
            padding: 1rem 0rem;
            display: table-row;
            vertical-align: inherit;
            unicode-bidi: isolate;
            border-color: inherit;
            }
            td {
            border: solid 0px black;
            padding: 0rem 2rem;
            }
            td:first-child {
            padding: 0rem 1rem;
            }
            th:last-child {
            padding: 0rem 1rem;
            }
            .body-container {
            height: 100%;
            width: 100%;
            }
            .table-container {
            display: flex;
            align-items: center;
            justify-content: center;
            }
        </style>
        """
        
        rows = ["""<tr id='%d'>
                <td id='%d-name'>%s</td>
                <td id='%d-type'>%s</td>
                <td id='%d-value'>%s</td>
                </tr>""" % (
                    pin['id'],
                    pin['id'],
                    pin['name'],
                    pin['id'], 
                    'on/off' if pin['type']==1 else 'range',
                    pin['id'],
                    getPinValue(pin))
                for pin in pins]
        response = html % ('\n'.join(rows), update_script + style)
        print(response)
        response = "HTTP/1.1 200 Ok \r\n" + "Content-Type: text/html\r\n" +"\r\n" + response
        return response

    def _handleGetPins(self, **params):
        response = []
        for pin in pins:
            response.append({'id': pin['id'], 'pinNumber': pin['pinNumber'], 'isReadOnly': pin['isReadOnly'], 'name': pin['name'], 'type': pin['type'], 'value': getPinValue(pin)})
        
        if 'id' in params:
            response = [pin for pin in response if int(pin['id']) == int(params['id'])]
        
        response = "HTTP/1.1 200 Ok \r\n" + "Content-Type: application/json\r\n" +"\r\n" + json.dumps(response)
        return response
    

    def _handleGetSensors(self, **params):
        response = [
            {'id': '12', "name": "Temperature sensor", "value": f"{read_temperature()}"}, 
            {'id': '11', "name": "Potentiometer", "value": f"{get_potentiometer_load()}"}]
        
        if 'id' in params:
            response = [sensor for sensor in response if int(sensor['id']) == int(params['id'])]
        
        response = "HTTP/1.1 200 Ok \r\n" + "Content-Type: application/json\r\n" +"\r\n" + json.dumps(response)
        return response
    
    def _handleEdit(self, **params):
        chosen_pin = None
        if 'pinId' in params:
            for pin in pins:
                if int(pin['id']) == int(params['pinId']):
                    chosen_pin = pin
                    break
        if chosen_pin is None:
            return "HTTP/1.1 422 Unprocessable entity \r\n" + "Content-Type: application/json\r\n" +"\r\n" + json.dumps({'status': 'pin id not found'})
        if chosen_pin['isReadOnly']:
            return "HTTP/1.1 422 Unprocessable entity \r\n" + "Content-Type: application/json\r\n" +"\r\n" + json.dumps({'status': 'pin %d is read-only' % chosen_pin['id']})
        
        # binary value pins
        if 'isOn' in params:
            is_on = params['isOn'].lower() == 'true'
            chosen_pin['pin'].value(is_on)
            
            return "HTTP/1.1 200 \r\n" + "Content-Type: application/json\r\n" +"\r\n" + json.dumps({'status': 'ok'})
        
        # pwm
        if 'pwmDutyLoad' in params:
            pwm_duty_load = float(params['pwmDutyLoad'])
            if pwm_duty_load < 0 or pwm_duty_load > 1:
                return "HTTP/1.1 422 Unprocessable entity \r\n" + "Content-Type: application/json\r\n" +"\r\n" + json.dumps({'status': 'pwm duty load must be between 0 and 1'})
            chosen_pin['pwm'].duty(int(pwm_duty_load * MAX_DUTY))
            
            return "HTTP/1.1 200 \r\n" + "Content-Type: application/json\r\n" +"\r\n" + json.dumps({'status': 'ok'})
            
        return  "HTTP/1.1 422 Unprocessable entity \r\n" + "Content-Type: application/json\r\n" +"\r\n" + json.dumps({'status': 'could not recognize the edit'})