#!/usr/bin/env python3


prefix = '/usr/local'
exports_file = prefix + '/share/usbip_services/settings.csv'


usbip_cmd = 'usbip'
usbipd_cmd = 'usbipd'

import csv
import pyudev
import time
import subprocess
import functools

# Need bufferless stdout for deamon.
print = functools.partial(print, flush = True)

# Run deamon process.
subprocess.run([usbipd_cmd, '-D'])

devs_for_export = {}
active_devs_for_export = {}
active_devs_for_export_busid = {}

context = pyudev.Context()
while True:
	with open(exports_file, newline = '') as csv_file:
		r = csv.reader(csv_file, delimiter='\t', quotechar='"')
		for row in r:
			t = row[0]
			if t == 'export/import':
				id = row[1]
				name = row[2]
				if id not in devs_for_export:
					devs_for_export[id] = name
					active_devs_for_export[id] = False

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
		#if ID == '16c0:05dc':
		#	for a in dev.attributes.available_attributes:
		#		print(a, ' : ', dev.attributes.get(a))

	for d in active_devs_for_export:
		if d in active_devs:
			if not active_devs_for_export[d]:
				active_devs_for_export[d] = True
				print("Binding {} {}".format(d, devs_for_export[d]))
				cmd = usbip_cmd + ' list -p -l'
				print("cmd = {}".format(cmd))
				r = subprocess.run(cmd.split(), stdout = subprocess.PIPE)
				so = r.stdout.decode('ascii')
				print("so = {}".format(so))
				l = so.split('\n')
				busid = None
				for ll in l:
					t = ll.split('#')
					if len(t) == 3 and t[1] == 'usbid='+d:
						busid = t[0]
				print("busid = {}".format(busid))
				if busid:
					active_devs_for_export_busid[d] = busid
					cmd = usbip_cmd + ' bind -b ' + busid[len('busid='):]
					print("cmd = {}".format(cmd))
					r = subprocess.run(cmd.split())
					print("r = {}".format(r))
		else:
			if active_devs_for_export[d]:
				active_devs_for_export[d] = False
				#print("Unbinding {} {}".format(d, devs_for_export[d]))
				#busid = active_devs_for_export_busid[d]
				#cmd = usbip_cmd + ' unbind --' + busid
				#r = subprocess.run(cmd.split())


	time.sleep(1)
