# DS18b20 temperature probe Python class for the one wire Linux driver
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


class ds18b20(object):

  def __init__(self, id):
    self._id = id 

  @property
  def temperature(self):
    try:
      f = open("/sys/bus/w1/devices/" + self._id + "/w1_slave")
    except IOError:
      return -273.0
    txt = f.read()
    f.close()

    temptxt = txt.split("\n")[1].split(" ")[9]
    return (float(temptxt[2:]) / 1000)
