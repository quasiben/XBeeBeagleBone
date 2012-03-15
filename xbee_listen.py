#! /usr/bin/python
import os 
import logging 

import serial
import time
from xbee import ZigBee
import xbee_at_cmds as at

PORT = '/dev/ttyO1'
BAUD_RATE = 9600

PORT = '/dev/ttyO1' #set tty port NOTE: ON BEAGLE BONE O1 is the Letter O
BAUD_RATE = 9600 #set baud rate

uart1_pin_mux = [
	('uart1_rxd', ( 0 | (1<<5) )), # Bit 5 sets the receiver to enabled for RX Pin
	('uart1_txd', ( 0 )),  #no bits to be set for TX Pin
]

for (fname, mode) in uart1_pin_mux:
	with open(os.path.join('/sys/kernel/debug/omap_mux', \
	fname), 'wb') as f: #easy open/writing/closing of file with 'with'
		f.write("%X" % mode)


#callbacks and threads
def dump(data):
    print data

def dump_back(data):
	if 'source_addr' in data:
        addr = data['source_addr']
        addr_long = data['source_addr_long']
        rf_data = "got the message (%s)" % data['rf_data']
        fid = data['options']
        print rf_data, " from ", str(data['source_addr_long'].encode("hex"))
        xbee.send('tx', frame_id=fid, dest_addr=addr, dest_addr_long=addr_long, data=rf_data)
    else:
        print data


serial_port = serial.Serial(PORT, BAUD_RATE)
xbee = ZigBee(serial_port, callback=dump_back, escaped=True)


xbee.send("at", frame_id='a', command='DH')
xbee.send("at", frame_id='a', command='DL')
xbee.send("at", frame_id='a', command='NI')
xbee.send("at", frame_id='a', command='MY')
print "------------------------------------------------------------------"
xbee.send("at", frame_id='a', command='ND')

# done
while True:
    try: 
        time.sleep(0.01)
    except KeyboardInterrupt:
        break



xbee.halt()
serial_port.close()

