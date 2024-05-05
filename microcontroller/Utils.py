from PinDefinitions import potentiometer_adc, i2c


MIN_POTENTIOMETER_VOLTAGE = 75*1000
MAX_POTENTIOMETER_VOLTAGE = 1063*1000
MAX_DUTY = 2**10-1

def get_potentiometer_load():
        voltage = potentiometer_adc.read_uv()
        
        voltage_load = (voltage - MIN_POTENTIOMETER_VOLTAGE) / (MAX_POTENTIOMETER_VOLTAGE - MIN_POTENTIOMETER_VOLTAGE) # value from 0 to 1
        voltage_load = min(voltage_load,1) # just make sure that it is within the range
        return round(voltage_load, 2)
        
def _convert_to_celcius(data):
    value = (data[0] << 8) | data[1]
    temp = (value & 0xFFF) / 16
    if value & 0x1000:
        temp -= 256
    return temp

def read_temperature():
    data = bytearray(2)
    i2c.readfrom_mem_into(24,5,data)
    temp = _convert_to_celcius(data)
    return temp