import machine
import network
import socket
import uasyncio
import json

from server.RequestParser import RequestParser
from server.RequestHandler import RequestHandler

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
        
        self.requestParser = RequestParser()
        self.requestHandler = RequestHandler()

        print('listening on', addr)

    """
    Starts the server
    """
    async def start(self):
        while True:
            await self._wait_and_process_request()
            await uasyncio.sleep_ms(1)
    
    """
    Checks for an incomming request in a nonblocking way. 
    Prectically it is done to achive asynchronous awaiting of the requests. 
    Despite the fact that it is not real async call, it serves its purpose and is the best possible approximation for awaiting requets in micropython.
    """
    async def _get_connection(self):
        try:
            return self.s.accept()
        except OSError as e:
            # Handle the case where no incoming connection is available
            if not (e.args[0] == errno.EAGAIN or e.args[0] == errno.EWOULDBLOCK):
                # Handle other OSError exceptions
                print("Error accepting connection:", e)
            return None

    """
    Check if there is an incoming request and process it.
    Processing is done by paring the request and using the qcquired information to call the right method which will handle it.
    """
    async def _wait_and_process_request(self):
            # check for an incoming connection
            connection_result = await self._get_connection()
            if connection_result is None:
                return
            cl, addr = connection_result
            print('client connected from', addr)

            # parse request
            request_type, endpoint_path, params = self.requestParser.get_request_info(cl)
            
            # perform a proper action to handle the request
            response = self.requestHandler.handle_request(request_type, endpoint_path, params)
            
            # return response and close
            cl.send(response)
            cl.close()

