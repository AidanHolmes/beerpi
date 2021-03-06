# BeerPi control code to manage Energenie sockets based on temperature
# Copyright (C) 2017 Aidan Holmes
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Email: aidanholmes@orbitalfruit.co.uk

import time
from ds18b20 import ds18b20
import ener
import mosquitto as mqtt

power = ener.Energenie()
is_connected = False
is_first = True
brew = [{"heater":False,"heatctl":1,"min":20,"max":21,"sensor":ds18b20("28-0517022710ff")},
        {"heater":False,"heatctl":2,"min":20,"max":21,"sensor":ds18b20("28-041702ce85ff")}]

def mqtt_connect(client, userdata, rc):
  global is_connected
  global is_first
  print("Connected with result code {}".format(rc))
  client.subscribe("beer/brew1/heater", 2)
  client.subscribe("beer/brew1/min_temp", 2)
  client.subscribe("beer/brew1/max_temp", 2)
  client.subscribe("beer/brew2/heater", 2)
  client.subscribe("beer/brew2/min_temp", 2)
  client.subscribe("beer/brew2/max_temp", 2)
  is_connected = True
  is_first = True 

def mqtt_disconnect(client, userdata, rc):
  global is_connected
  global is_first
  is_connected = False
  is_first = False
  
def on_message(client, userdata, msg):
  global brew

  if msg.topic[:9] == "beer/brew":
    try:
      brewnum = int(msg.topic[9])
      attr = (msg.topic.split("/")[:1:-1])[0]
      if attr == "heater":
        brew[brewnum-1]["heater"] = (msg.payload == "on")
        power.switch(brewnum, brew[brewnum-1]["heater"])
      elif attr == "min_temp":
        brew[brewnum-1]["min"] = float(msg.payload)
      elif attr == "max_temp":
        brew[brewnum-1]["max"] = float(msg.payload)
    except ValueError:
      pass
    except EnerError:
      pass
    
while 1:
  try:
    if not is_connected:
      client= mqtt.Mosquitto()
      client.on_connect = mqtt_connect
      client.on_message = on_message
      client.on_disconnect = mqtt_disconnect
      client.will_set("beer/server", "offline", 2, True)
      client.connect_async("192.168.1.200")
      client.loop_start()
    # end if is_connected

    if is_connected:
      if is_first:
        client.publish("beer/server", "online", 2, True)
        is_first = False
      # end if is_first

      # Iterate through sensors
      for s in range(len(brew)):
        temp = brew[s]["sensor"].temperature
        client.publish("beer/brew{0}/temperature".format(s+1), temp)

        # Check temperature. Set heater
        if temp != -273.0:
          try:
            if brew[s]["min"] > temp and not brew[s]["heater"]:
              brew[s]["heater"] = True
              client.publish("beer/brew{0}/heater".format(s+1), "on", 2, True)
            elif brew[s]["max"] < temp and brew[s]["heater"]:
              brew[s]["heater"] = False
              client.publish("beer/brew{0}/heater".format(s+1), "off", 2, True)
            # end if
          except KeyError:
            pass
          except IndexError:
            pass
          # end try
        # end if

      # Control heater. Keep sending the signal since it isn't reliable
      for i in range(len(brew)):
        try:
          power.switch(brew[i]["heatctl"], brew[i]["heater"])
          #time.sleep(0.1) # Small sleep between switches
        except EnerError:
          print("Error switching brew {0}".format(brew[i]["heatctl"]))
        # end try
      # end for

    # Pause for 5 seconds and read again
    time.sleep(5)

  except KeyboardInterrupt:
    power.cleanup()
    client.loop_stop()
    if (is_connected):
      client.disconnect()
    quit()
  except SocketError as e:
    is_connected = False
    is_first = False
    if e.errno == errno.ECONNRESET:
      print ("Connection reset, attepmting to reconnect in 30 sec...")
      time.sleep(30)
    else:
      print ("A problem occurred with the connection. Attemping to reconnect in 5 min")
      time.sleep(300)
  # end try
# end loop while 1
