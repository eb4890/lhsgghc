import socket
import select
import struct
import json

MCAST_GRP = '224.1.1.1'


def listen(controller, port):
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.bind(('', port))

  mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
  s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
  s.setblocking(0)

  while True:
    try:
      result = select.select([s],[],[])
      payload = result[0][0].recv(1024)
      print 'Recv: %s' % repr(payload)

      event = json.loads(payload.decode('UTF-8'))
      print 'Received event: %s' % repr(event)

      if event['event'] in controller:
        controller[event['event']](event)

    except Exception, e:
      print 'Exception receiving: %s' % repr(e)

def broadcast(msg, port):

  try:
    msg = msg.encode('UTF-8')
    print 'Send: %s' % (repr(msg))

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    s.sendto(msg, (MCAST_GRP, port))

  except Exception, e:
    print 'Exception sending: %s' % repr(e)
