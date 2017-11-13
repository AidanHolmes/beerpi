# BeerPi
Beer temperature control with Energenie and DS18B20 libraries

## control.py
Control uses MQTT libraries to communicate status and accept input
> apt-get install python-mosquitto

Beer monitoring constantly (every 5 seconds) checks temperature from DS18b20 probes and maintains a temperature range.
If the connection is lost to the MQTT server the code will continue with the last settings and still enable/disable the heaters.

Heater control uses the Energenie (https://energenie4u.co.uk/) radio sockets and Pi-mote.
There is no guarantee that a socket will switch if there is interference or working at a distance from the socket.
The control code therefore constantly sends the on/off signals to the sockets.

Sensor IDs and MQTT connection details are hardcoded. Alter to fit your configuration

### MQTT topics used.
? indicates where the brew number is specified

Direction | Topic | Notes
--- | --- | ---
OUT | beer/server | a string with `offline` or `online`
IN/OUT | beer/brew?/heater | a string with `on` or `off`. This value can be set
IN | beer/brew?/min_temp | a float value set to min temp value (heater triggered to enable)
IN | beer/brew?/max_temp | a float value set to max temp value (heater triggered to disable)
OUT | beer/brew?/temperature | a float value of the current temperature

## ds18b20.py
Drivers need to be enabled in /boot/config.txt
Add lines
> \# Temp sensor
> dtoverlay=w1-gpio,gpiopin=4


This is a basic class for the temperature probes. Assumes that the driver sets
> /sys/bus/w1/devices/

### __init__
ds18b20 objects are created with the ID from `/sys/bus/w1/devices/`. Each ID is unique to the temperature sensor.

### temperature
This is a property of the created object. This is only to read the temperature from the sensor in °C.
If the temperature cannot be read then -273 is returned.

## ener.py
This class represents the Pi-mote device for the Raspberry Pi. 
Uses the RPi GPIO python library.

### __init__
Pins are fixed for the Pi-mote and can not be changed in initialisation.
Creation of an object sets up all the GPIO pins. Only 1 object can exist

### cleanup()
Call this to clean up the GPIO

### switchall(onoff)
onoff is a boolean value. This will enable or disable all registered sockets
**Note** that this call is unreliable if the radio transmission is out of range or lost due to interference.

### switch(num, onoff)
Individually switch on or off sockets. Sockets are numbered 1, 2, 3 or 4. Use of other num values will throw an exception.
onoff is a boolean value to enable or disable the socket
**Note** that this call is unreliable if the radio transmission is out of range or lost due to interference.


