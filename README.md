# tipower-portal

## Overview

get the smartmeter data over m-bus from a kaifa tinetz smartmeter and save it to influxdb and display the data with grafana

## Requirements Hardware

 - [M-Bus Adapter USB](https://www.amazon.de/ZTSHBK-USB-zu-MBUS-Slave-Modul-Master-Slave-Kommunikation-Debugging-Bus%C3%BCberwachung/dp/B09F5FGYVS/)
 - [M-Bus Adapter SERIAL](https://www.mikroe.com/m-bus-slave-click)
 - [Wiring Smartmeter -> RJ12 -> M-Bus Adapter](https://github.com/tirolerstefan/kaifa/blob/master/img/connection.png)

## Requirements Software

`apt update`  
`apt install python3-serial python3-pycryptodome python3-requests`

## Install

`mkdir src`  
`cd src/`  
`git clone https://github.com/lukasdebaum/tipower-kaifa`  
`mv tipower-kaifa /opt/`  
`cd /opt/tipower-kaifa/`  
`cp tipower_kaifa.service /etc/systemd/system/tipower_kaifa.service`  
`cp example_config.py config.py`  

edit `config.py` with your favorite editor

## Config

### serial_port
serial port in linux dev
 - `/dev/ttyUSB0` (for usb adapter)
 - `/dev/ttyAMA0` (for serial adaper, disable rpi serial console!)

### device
smartmeter name for influxdb device tag

### key
"Kundenschnittstellen Zugangscode"  
smartmeter AES key, format: 685A...  
can be requested via the tinetz customer portal https://kundenportal.tinetz.at/

### db_name 
influx db name

### interval
interval in seconds when the aggregated values send to the influxdb

## systemd service

reload systemd  
`systemctl daemon-reload`  

activate tipower_kaifa service on boot  
`systemctl enable tipower_kaifa.service`  

start tipower_kaifa service  
`systemctl start tipower_kaifa.service`  

show status of service (check if tipower_kaifa runs)  
`systemctl status tipower_kaifa.service`  

## ToDo

 - add influxdb authentication

## Thanks
 - https://github.com//peerdavid/smartmeter-ha
 - https://github.com/tirolerstefan/kaifa/
 - https://www.tinetz.at/uploads/tx_bh/tinetz_smart-meter_beschreibung-kundenschnittstelle_001.pdf
