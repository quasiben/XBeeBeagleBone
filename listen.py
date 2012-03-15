#!/usr/bin/env python

import serial, os
import sys

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


ser = serial.Serial(PORT, BAUD_RATE) #open serial port
count = 0
while True:
	a = ser.read() #read byte
	print count, a #print byte and count
	count += 1