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
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.bind(('<broadcast>', port))
  s.setblocking(0)
  while True:
    try:
      result = select.select([s],[],[])
      payload = result[0][0].recv(1024)
      print "Total Message = %s" % payload
      (event, args) = payload.split("\n")
      print "Received event: %s with args %s" % (event, args)  
      controller[event](args)          
    except Exception as a:
      print a
      pass



def broadcast(event, args, port):

    try:
        print "Broadcasting %s to network with args %s" % (event, args)

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        data = "%s\n%s" % (event, args)
        s.sendto(data, ('<broadcast>', port))

    except Exception, e:
        pass

