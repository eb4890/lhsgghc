import socket
import select
import struct
import json

#from calendar import calendar

'''
Resources

startlesson
nextquestion
endlesson (called auto after last nextfeedback)? 
updatedisplay

onfeedback
'''
MCAST_GRP = '224.1.1.1'

class Message():
  def __init__(self, devid, event):
    self.devid = devid
    self.event = event

def parseMessage(event, data):
  m =  Message( ButtonPress(data).buzzerid, data)
  
  return m

def setlight(devid,value):
  gl.broadcast("""{"event": "setlight" , "devid":"%s", "state": "%s"}""" % (devid, value) , 50001)
 

  
class ComposeDespatch():
  def __init__(self, dispatchone, dispatchtwo):
    self.d1 = dispatchone
    self.d2 = dispatchtwo

  def __getitem__(self, index):
    if index in self.d1: 
      return self.d1[index]
    elif index in self.d2:
      return self.d2[index]
    else: 
      raise KeyError
  
 
  def __setitem__(self,index, value):
    if index in self.d1:
      self.d1[index] = value
    elif index in self.d2:
      self.d2[index] = value
    else:
      self.d1[index] = value
     

class Association():
  def __init__(self, key=None, value=None, string=""):
    if key != None and value != None: 
      self.key = key
      self.value = value
    elif string != "":
      arr = string.split(":")
      self.key = arr[0]
      self.value = arr[1] 
  
  def toText(self):
    return "%s:%s" % (self.key,self.value)

class ButtonPress (): 
   def __init__(self, args="", dictionary ={}):
     if (args != ""):
       self.button, self.buzzerid, self.timestamp = args.split(':')
     elif dictionary != {}:
 
       self.buzzerid = dictionary[buzzerid]
       self.timestamp = dictionary[timestamp]
       self.button = dictionary[button]

def listen(controller, port):
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.bind(('', port))
  
  mreq =  struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
  s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
  s.setblocking(0)
  while True:
    try:
      result = select.select([s],[],[])
      payload = result[0][0].recv(1024)
      print "Total Message = %s" % payload
      data = json.loads(payload.decode("UTF-16"))
      #data2  = json.loads(data)
      #data3 = json.loads(data)
      print data
      for (k,v) in data.items():
        print k + " " + v
      print "Received event: %s with args %s" % (data["event"], data)  
      if data["event"] in controller: 
        controller[data["event"]](data)          
    except Exception as a:
      print a
      pass



def broadcast(event, port):

    try:
        print "Broadcasting %s to network" % (event)

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        #s.bind(('', 0))
        #s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        #data = "%s\n%s" % (event, args)
        text = event.encode("UTF-16")
        #print text
        s.sendto(text, (MCAST_GRP, port))

    except Exception, e:
        print e
        pass

