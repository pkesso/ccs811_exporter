#!/usr/bin/env python3

from time import sleep
from Adafruit_CCS811 import Adafruit_CCS811
from prometheus_client import start_http_server, Summary,Gauge

port = 8002

ccs = Adafruit_CCS811()

while not ccs.available():
    pass
temp = ccs.calculateTemperature()
ccs.tempOffset = temp - 25.0

co2 = Gauge('ccs811_co2', 'CO2 level, ppm')
tvoc = Gauge('ccs811_tvoc', 'Total Volatile Organic Compounds level, ppm')
temperature = Gauge('ccs811_temperature', 'Air temperature, C')

REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

@REQUEST_TIME.time()
def get_data():
    if ccs.available():
        temp = ccs.calculateTemperature()
        if not ccs.readData():
            #print("CO2: ", ccs.geteCO2(), "ppm, TVOC: ", ccs.getTVOC(), " temp: ", temp)
            temperature.set(ccs.calculateTemperature())
            co2.set(ccs.geteCO2())
            tvoc.set(ccs.getTVOC())
        else:
            print(datetime.now(), " ERROR!")
            while(1):
                pass
    

if __name__ == '__main__':
    start_http_server(port)
    while True:
        get_data()
        sleep(1)

