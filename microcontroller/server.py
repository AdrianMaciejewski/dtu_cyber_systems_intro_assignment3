import machine
import network
import socket
import uasyncio
import json

from PinDefinitions import button_led_pin, green_led_pin, orange_led_pin, red_led_pin, rgb_led_red_pin, rgb_led_green_pin, rgb_led_blue_pin, sda_pin, scl_pin, potentiometer_pin, button_change_task, red_pwm, green_pwm, blue_pwm, pins, i2c
from Task3 import read_temperature

class Server():
    def __init__(self):
        # Create wifi network
        self.ap = network.WLAN (network.AP_IF)
        self.ap.active (True)
        self.ap.config (essid = 'ESP32-WIFI-NAME')
        self.ap.config (authmode = 3, password = 'WiFi-password')
        
        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        self.s = socket.socket()
        self.s.bind(addr)
        self.s.listen(1)
        # Set the server socket to be non-blocking
        self.s.setblocking(False)


        print('listening on', addr)


        self.endpoints = {'/': {'get': self.GetPinsView}, '/pins': {'get': self.GetPins}, '/sensors': {'get': self.GetSensors}, '/edit': {'get': self.HandleEdit}}

    def _get_connection(self):
        try:
            return self.s.accept()
        except OSError as e:
            # Handle the case where no incoming connection is available
            if not (e.args[0] == errno.EAGAIN or e.args[0] == errno.EWOULDBLOCK):
                # Handle other OSError exceptions
                print("Error accepting connection:", e)
            return None

    
    async def _wait_and_process_request(self):
            connection_result = self._get_connection()
            if connection_result is None:
                return

            cl, addr = connection_result
            print('client connected from', addr)

            request_type, endpoint_path, params = self.get_request_info(cl)
            
            response = "HTTP/1.1 404 Not found \r\n" + "Content-Type: text/html\r\n" +"\r\n"
            if endpoint_path.lower() in self.endpoints:
                if request_type.lower() in self.endpoints[endpoint_path]:
                    response = self.endpoints[endpoint_path.lower()][request_type.lower()](**params)
            elif endpoint_path.lower().startswith('/edit'):
                if request_type.lower() in self.endpoints[endpoint_path]:
                    response = self.endpoints['/edit'][request_type.lower()](**params)
            
            # return template
            cl.send(response)
            cl.close()
    
    
    def get_request(self, cl):
        cl_file = cl.makefile('rwb', 0)
        request = ""
        while True:
            line = cl_file.readline()
            request += line.decode("utf-8")
            if not line or line == b'\r\n':
                break
        print(request)
        return request

    async def start(self):
        while True:
            await self._wait_and_process_request()
            await uasyncio.sleep_ms(1)

    def get_request_info(self, cl):
        request = self.get_request(cl)

        request_info = request.splitlines()[0].split(' ')
        request_type = request_info[0]
        request_path = request_info[1]
        
        endpoint_path, params = self.get_path_and_params_from_url(request_path)
            
        return request_type, endpoint_path, params

    def get_path_and_params_from_url(self, path):
        endpoint_path = path
        query_pos = endpoint_path.find('?')
        if query_pos != -1:
            query_string = endpoint_path[query_pos + 1:]  # Extract query string
            endpoint_path = endpoint_path[:query_pos]  # Extract path
            params = dict(param.split('=') for param in query_string.split('&'))  # Parse query parameters
        else:
            params = {}
            
        return endpoint_path, params
    

    def GetPinsView(self, **params):
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
        pins = {'Button led pin' : button_led_pin, 'Green led pin' : green_led_pin, 'Orange led pin' : orange_led_pin, 'Red led pin' : red_led_pin, 'RGB led red pin' : rgb_led_red_pin, 'RGB led green pin' : rgb_led_green_pin, 'RGB led blue pin' : rgb_led_blue_pin, 'SDA pin' : sda_pin, 'SCL pin' : scl_pin, 'Potentiometer pin' : potentiometer_pin, 'Button change task' : button_change_task}
        rows = ['<tr><td>%s</td><td>%d</td></tr>' % (name, pin.value()) for name, pin in pins.items()]
        response = html % ('\n'.join(rows), style)
        
        response = "HTTP/1.1 200 \r\n" + "Content-Type: text/html\r\n" +"\r\n" + response
        return response

        

    def GetPins(self, **params):
        response = []
        for pin in pins:
            response.append({'id': pin['id'], 'name': pin['name'], 'type': pin['type'], 'pin_value': pin['pin'].value(), 'pwm_duty': pin['pwm'].duty() if pin['pwm'] is not None else None})
        
        if 'id' in params:
            response = [pin for pin in response if int(pin['id']) == int(params['id'])]
        
        response = "HTTP/1.1 200 \r\n" + "Content-Type: application/json\r\n" +"\r\n" + json.dumps(response)
        return response
    

    def GetSensors(self, **params):
        response = [{'id': '1', "name": "Temperature sensor", "value": f"{read_temperature(i2c)}"}]
        
        if 'id' in params:
            response = [sensor for sensor in response if int(sensor['id']) == int(params['id'])]
        
        response = "HTTP/1.1 200 \r\n" + "Content-Type: application/json\r\n" +"\r\n" + json.dumps(response)
        return response
    
    def HandleEdit(self, **params):
        chosen_pin = None
        if 'pinId' in params:
            for pin in pins:
                if int(pin['id']) == int(params['pinId']):
                    chosen_pin = pin
                    break
        if chosen_pin is None:
            return "HTTP/1.1 404 \r\n" + "Content-Type: application/json\r\n" +"\r\n" + json.dumps({'status': 'pin id not found'})
        
        
        # binary value pins
        if 'isOn' in params:
            is_on = params['isOn'].lower() == 'true'
            chosen_pin['pin'].value(is_on)
            
            return "HTTP/1.1 200 \r\n" + "Content-Type: application/json\r\n" +"\r\n" + json.dumps({'status': 'ok'})
        
        # pwm
        if 'pwmDutyLoad' in params:
            pwm_duty_load = float(params['pwmDutyLoad'])
            if pwm_duty_load < 0 or pwm_duty_load > 1:
                return "HTTP/1.1 400 \r\n" + "Content-Type: application/json\r\n" +"\r\n" + json.dumps({'status': 'pwm duty load must be between 0 and 1'})
            chosen_pin['pwm'].duty(int(pwm_duty_load * 1023))
            
            return "HTTP/1.1 200 \r\n" + "Content-Type: application/json\r\n" +"\r\n" + json.dumps({'status': 'ok'})
            
        return  "HTTP/1.1 404 \r\n" + "Content-Type: application/json\r\n" +"\r\n" + json.dumps({'status': 'could not recognize the edit'})