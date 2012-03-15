#!/usr/bin/env python

import serial, os
import sys, logging

PORT = '/dev/ttyO1'
BAUD_RATE = 9600

uart1_pin_mux = [
	('uart1_rxd', ( 0 | (1<<5) )),
	('uart1_txd', ( 0 )),
]

logging.basicConfig(level=logging.DEBUG)

for (fname, mode) in uart1_pin_mux:
	logging.debug("%s = %s" % (fname, mode))
	with open(os.path.join('/sys/kernel/debug/omap_mux', \
	fname), 'wb') as f:
		f.write("%X" % mode)

# Open serial port
ser = serial.Serial(PORT, BAUD_RATE)
count = 0
while True:
	a = ser.read()
	print count, a
	count += 1