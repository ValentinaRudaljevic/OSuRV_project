# OSuRV_project

******************************************************************************************

Client is RPI and server is PC. Client and server are connected via WiFi.
Available USB devices connected on server side will be visible on client side.

******************************************************************************************

Instructions:
- Open two terminals - one for client and one for server

- Insert joystick, as USB device, on your PC

- Run usbip.service and usbipd.service as background subprocesses

- Run install.sh scripts on client and server side

- Now joystick should be visible on client side; check with "lsusb" command

- On client side type "jstest /dev/input/<joystick_device>" command and use the joystick 

******************************************************************************************
