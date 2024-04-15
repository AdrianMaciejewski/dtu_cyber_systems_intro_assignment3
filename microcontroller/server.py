import machine
import network
import socket
import uasyncio

from PinDefinitions import button_led_pin, green_led_pin, orange_led_pin, red_led_pin, rgb_led_red_pin, rgb_led_green_pin, rgb_led_blue_pin, sda_pin, scl_pin, potentiometer_pin, button_change_task

class Server():
    def __init__(self):
        self.html = """
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
        self.style = """
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
        self.pins = {'Button led pin' : button_led_pin, 'Green led pin' : green_led_pin, 'Orange led pin' : orange_led_pin, 'Red led pin' : red_led_pin, 'RGB led red pin' : rgb_led_red_pin, 'RGB led green pin' : rgb_led_green_pin, 'RGB led blue pin' : rgb_led_blue_pin, 'SDA pin' : sda_pin, 'SCL pin' : scl_pin, 'Potentiometer pin' : potentiometer_pin, 'Button change task' : button_change_task}

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

            cl_file = cl.makefile('rwb', 0)
            while True:
                line = cl_file.readline()
                print(line)
                if not line or line == b'\r\n':
                    break

            # return template
            rows = ['<tr><td>%s</td><td>%d</td></tr>' % (name, pin.value()) for name, pin in self.pins.items()]
            response = self.html % ('\n'.join(rows), self.style)
            cl.send(response)
            cl.close()

    async def start(self):
        while True:
            await self._wait_and_process_request()
            await uasyncio.sleep_ms(1)
    
