# BeerPi terminal monitor to print temperature
# Copyright (C) 2018 Aidan Holmes
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

from ds18b20 import ds18b20
import time

brew = [{"heater":False,"heatctl":1,"min":20,"max":21,"sensor":ds18b20("28-0517022710ff")},
        {"heater":False,"heatctl":2,"min":20,"max":21,"sensor":ds18b20("28-041702ce85ff")}]

try:

  while 1:
    # Iterate through sensors
    for s in range(len(brew)):
      temp = brew[s]["sensor"].temperature
      print("Brew {0}: Temperature {1}".format(s+1, temp))

    # Pause for 5 seconds and read again
    time.sleep(5)
 
except KeyboardInterrupt:
  pass
