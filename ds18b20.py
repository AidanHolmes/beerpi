# Copyright Aidan Holmes 2017


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
