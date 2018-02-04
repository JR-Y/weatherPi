

class Sensors:
  def __init__(self, gpio, name):
      self.gpio = gpio
      self.name = name

dht = [Sensors(4,'Ulkoanturi'),Sensors(17,'Sisäanturi')]


for i in range(len(dht)):
  print (str(dht[i].gpio) + ' ' + dht[i].name)
