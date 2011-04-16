import socket
import select
import struct
import json

MCAST_GRP = '224.1.1.1'


def multisocket(port):
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.bind(('', port))

  mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
  s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
  s.setblocking(0)

  return s

class MessageListener():

  def __init__(self, port):
    self.port = port
    self.controller = {}
    self.multisocket = multisocket(self.port)

  def handle_msg(self, msg):
    event = json.loads(msg.decode('UTF-8'))
    print 'Received event: %s' % repr(event)

    try:
      handler = controller[event['event']]
    except KeyError, e:
      print 'Unknown event %s' % repr(event['event'])
      return

    try:
      handler(event)
    except Exception, e:
      print 'Exception handling %s: %s' % (event['event'], repr(e))

  def run():
    while True:
      try:
        socks = [self.multisocket]
        readers, writers, errors = select.select(socks, [], [])
        msg = readers[0][0].recv(1024)
        print 'Recv: %s' % repr(msg)

      except Exception, e:
        print 'Exception receiving: %s' % repr(e)

      self.handle_msg(msg)


def broadcast(msg, port):

  try:
    msg = msg.encode('UTF-8')
    print 'Send: %s' % (repr(msg))

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    s.sendto(msg, (MCAST_GRP, port))

  except Exception, e:
    print 'Exception sending: %s' % repr(e)
