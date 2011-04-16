import network

class ButtonPress ():
  def __init__(self, args="", dictionary ={}):
    if (args != ""):
      self.button, self.buzzerid, self.timestamp = args.split(':')
    elif dictionary != {}:

      self.buzzerid = dictionary[buzzerid]
      self.timestamp = dictionary[timestamp]
      self.button = dictionary[button]

class Message():
  def __init__(self, devid, event):
    self.devid = devid
    self.event = event

def parseMessage(event, data):
  m = Message(ButtonPress(data).buzzerid, data)
  return m

def setlight(devid, value):

  ev = {
    'event': 'setlight',
    'devid': devid,
    'state': value,
  }
  network.broadcast(ev, 50001)

