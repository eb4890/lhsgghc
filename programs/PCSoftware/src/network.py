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
    except Exception, e:
      print e

def broadcast(event, port):

  try:
      print "Broadcasting %s to network" % (repr(event))

      s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
      s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
      #s.bind(('', 0))
      #s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

      #data = "%s\n%s" % (event, args)
      event = json.dumps(event)
      text = event.encode("UTF-16")
      #print text
      s.sendto(text, (MCAST_GRP, port))

  except Exception, e:
      print e
