import network
import json

class ButtonPress ():
  def __init__(self, args="", dictionary={}):

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

def parse(event):
  m = Message(ButtonPress(event).buzzerid, event)
  return m

def send(event, port):
  msg = json.dumps(event)
  network.broadcast(msg, port)

def setlight(devid, value):

  ev = {
    'event': 'setlight',
    'devid': devid,
    'state': value,
  }
  send(ev, 50001)
