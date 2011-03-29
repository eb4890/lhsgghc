import socket
import select



#from calendar import calendar

'''
Resources

startlesson
nextquestion
endlesson (called auto after last nextfeedback)? 
updatedisplay

onfeedback
'''


def listen(controller, port):
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.bind(('<broadcast>', port))
  s.setblocking(0)
  while True:
    try:
      result = select.select([s],[],[])
      payload = result[0][0].recv(1024)
      (event, args) = payload.split("\n")
      controller[event](args)          
    except Exception as a:
      print a
      pass



def broadcast(event, args, port):

    try:
        print "Broadcasting %s to network" % event

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        data = "%s\n%s" % (event, args)
        s.sendto(data, ('<broadcast>', port))

    except Exception, e:
        pass

