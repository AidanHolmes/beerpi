# Energenie Python class to manage the Pi-mote
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

import RPi.GPIO as GPIO
import time

class EnerError(Exception):
        'Standard error class for Energenie Control'

        def __init__(self, err):
                self.value = err
                
        def __str__(self):
                return repr(self.value)
        
class Energenie(object):
        
        def __init__(self):
                # set the pins numbering mode
                GPIO.setmode(GPIO.BOARD)

                # Select the GPIO pins used for the encoder K0-K3 data inputs
                GPIO.setup(11, GPIO.OUT)
                GPIO.setup(15, GPIO.OUT)
                GPIO.setup(16, GPIO.OUT)
                GPIO.setup(13, GPIO.OUT)

                # Select the signal to select ASK/FSK
                GPIO.setup(18, GPIO.OUT)

                # Select the signal used to enable/disable the modulator
                GPIO.setup(22, GPIO.OUT)

                # Disable the modulator by setting CE pin lo
                GPIO.output (22, False)

                # Set the modulator to ASK for On Off Keying 
                # by setting MODSEL pin lo
                GPIO.output (18, False)

                # Initialise K0-K3 inputs of the encoder to 0000
                GPIO.output (11, False)
                GPIO.output (15, False)
                GPIO.output (16, False)
                GPIO.output (13, False)

        def cleanup(self):
                GPIO.cleanup()

        def switchall(self, onoff):
                cmd = [True, True, False, onoff]
                self.switchraw(cmd)
                
        def switch(self, num, onoff):
                cmd = [0,0,0,onoff]
                if (num == 1):
                        cmd = [True,True,True,onoff]
                elif(num == 2):
                        cmd = [False,True,True,onoff]
                elif(num == 3):
                        cmd = [True,False,True,onoff]
                elif(num == 4):
                        cmd = [False,False,True,onoff]
                else:
                        raise EnerError("Switch number out of range")

                self.switchraw(cmd)
                
        def switchraw(self, cmd):
                GPIO.output(11, cmd[0])
                GPIO.output(15, cmd[1])
                GPIO.output(16, cmd[2])
                GPIO.output(13, cmd[3])

                time.sleep(0.1)
                # Enable the modulator
                GPIO.output (22, True)
                # keep enabled for a period
                time.sleep(0.25)
                # Disable the modulator
                GPIO.output (22, False)
                                                                                                                
                
