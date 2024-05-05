import machine
import network
import socket
import uasyncio
import json

"""
Parses the request and extracts useful information.
"""
class RequestParser:
    """
    Gets information about a received request
    request_type - GET, POST etc.
    endpoint_path - e.g. for http://192.168.4.1/pins?id=13 it would be /pins
    params - e.g. for http://192.168.4.1/pins?id=13 it would be {'id': '13'}
    """
    def get_request_info(self, cl):
        request = self._get_request(cl)
        
        request_info = request.splitlines()[0].split(' ')
        request_type = request_info[0]
        request_path = request_info[1]
        
        endpoint_path, params = self._get_path_and_params_from_url(request_path)
            
        return request_type, endpoint_path, params
    
    """
    Reads the headers from the request and returns them as a single string.
    It assumes that the request headers are of a moderately short length, otherwise the device will crash due to the lack of memory. 
    """
    def _get_request(self, cl):
        cl_file = cl.makefile('rwb', 0)
        request = ""
        while True:
            line = cl_file.readline()
            request += line.decode("utf-8")
            if not line or line == b'\r\n':
                break
        print(request)
        return request

    """
    parses the requested path into requested endpoint and request parameters.
    E.g. http://192.168.4.1/pins?id=13 is parsed into:
     1. endpoint_path=/pins
     2. params={'id': '13'}
    """
    def _get_path_and_params_from_url(self, path):
        endpoint_path = path
        query_pos = endpoint_path.find('?')
        if query_pos != -1:
            query_string = endpoint_path[query_pos + 1:]  # Extract query string
            endpoint_path = endpoint_path[:query_pos]  # Extract path
            params = dict(param.split('=') for param in query_string.split('&'))  # Parse query parameters
        else:
            params = {}
            
        return endpoint_path, params
    