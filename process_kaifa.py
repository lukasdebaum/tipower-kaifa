#!/usr/bin/env python3

import sys
import signal
import serial
import time
import requests

import kaifa
import config

def signal_handler(sig, frame):
    serial_conn.close()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def print_e(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def write_influx(aggregate_data):
    influx_data_pack = list()

    for measurement in aggregate_data:
        if 'energy' in measurement:
            measurement_value = round(max(aggregate_data[measurement]), 2)
        else:
            measurement_value = round(sum(aggregate_data[measurement]) / len(aggregate_data[measurement]), 2)
        influx_data = f"smartmeter,device={config.device} {measurement}={measurement_value}"
        influx_data_pack.append(influx_data)

    influx_data_pack_format = '\n'.join(influx_data_pack)
    #print(influx_data_pack_format)

    try:
        r = requests.post(f"http://localhost:8086/write?db={config.db_name}", data=influx_data_pack_format)
        r.raise_for_status()
    except requests.exceptions.RequestException as err:
        print ("error: request error - %s" % (err))
        return False
    except requests.exceptions.HTTPError as errh:
        print ("error: request Http Error - %s" % (errh))
        return False
    except requests.exceptions.ConnectionError as errc:
        print ("error: request Connecting - %s" % (errc))
        return False
    except requests.exceptions.Timeout as errt:
        print_e("error: request timeout - %s" % (errt))
        return False
    if r.status_code != 204:
        print_e("error: request failed status code - %s" % (r.text))
        return False

    return True

serial_conn = serial.Serial(
    port = config.serial_port,
    baudrate = 2400,
    parity = serial.PARITY_EVEN,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 2
)

aggregate_data = dict()
time_now = time.time()
time_last = time.time()
while True:
    energy_object = kaifa.read_energy_data(serial_conn, config.key)
    #print(energy_object)
    del energy_object.data['datetime']

    for measurement in energy_object.data:
        if not measurement in aggregate_data:
            aggregate_data[measurement] = list()
        aggregate_data[measurement].append(energy_object.data[measurement])

    time_now = time.time()
    if time_now - time_last >= config.interval - 1:
        time_last = time.time()
        write_influx(aggregate_data)
        aggregate_data = dict()
