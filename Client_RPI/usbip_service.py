#!/usr/bin/env python3


prefix = '/usr/local'
exports_file = prefix + '/share/usbip_services/settings.csv'

#TODO Anoying log:
#usbip: info: no exportable devices found on
#
usbip_cmd = 'usbip'

import csv
import pyudev
import time
import subprocess
import functools
import re

# Need bufferless stdout for deamon.
print = functools.partial(print, flush = True)

devs_to_import = {}
SERVER_IP = None

context = pyudev.Context()
while True:
	with open(exports_file, newline = '') as csv_file:
		r = csv.reader(csv_file, delimiter='\t', quotechar='"')
		for row in r:
			t = row[0]
			if t == 'SERVER_IP':
				SERVER_IP = row[1]
			elif t == 'export/import':
				id = row[1]
				name = row[2]
				if id not in devs_to_import:
					devs_to_import[id] = name
	
	active_devs = []
	devices = context.list_devices(subsystem = 'usb') 
	for dev in devices:
		VID = dev.attributes.get('idVendor')
		PID = dev.attributes.get('idProduct')
		if VID == None or PID == None:
			continue
		VID = VID.decode('ascii')
		PID = PID.decode('ascii')
		ID = VID + ':' + PID
		active_devs.append(ID)
		##if ID == '0079:0006':
		##	for a in dev.attributes.available_attributes:
		##		print(a, ' : ', dev.attributes.get(a))
	
	for d in devs_to_import.keys():
		if d not in active_devs:
			
			cmd = [
				usbip_cmd, 'list',
				'-r', SERVER_IP
			]
			r = subprocess.run(cmd, stdout = subprocess.PIPE)
			so = r.stdout.decode('ascii')
			l = so.split('\n')
			busid = None
			for ll in l:
				m = re.match('\s*(.*):.*:.*\((.*)\)', ll)
				if m:
					if m.group(2) == d:
						busid = m.group(1)
			if busid:
				print("Attaching {} {}".format(d, devs_to_import[d]))
				cmd = usbip_cmd + ' -d attach -r ' + SERVER_IP + ' local -b ' + busid
				print("cmd = {}".format(cmd))
				r = subprocess.run(cmd.split())
				print("r = {}".format(r))
	
	time.sleep(1)
