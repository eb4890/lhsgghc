from twisted.internet import protocol, defer
from twisted.application import service
from twisted.python import log
from twisted.web import static, resource, server as webserver

import struct
import genericlib as gl


multicastgroup = "224.0.0.1"

def updateComet(request, message):
   request.write("{data: '%s'}" % message.event)
   request.finish()

class multicastProtocol(protocol.DatagramProtocol):
  
 
  def startProtocol(self):
    self.transport.joinGroup(multicastgroup)
    #self.transport.connect(self.service.multicastHost,self.service.multicastPort)
    #self.sendMessage("Send me data")
  def stopProtocol(self):
    return
  def datagramReceived(self,datagram,addr):
    try:
      print datagram
      event, data = datagram.split("\n")
      message = gl.parseMessage(event, data)
      self.mainHandler.sendCometMessage(message)
      print "Found" + event + data
    except Exception as err:
      log.err()
      return
 # def sendMessage(self,message):
  # self.transport.write(message)

#class 

class Button(resource.Resource):
  def __init__(self, event, devid):
    resource.Resource.__init__(self)
    self.buttonname = event
    self.devid = devid
  
  def render_GET(self, request):
    print "In Button"
    gl.broadcast("rawbuttonpress", "%s:%s:%s" % (self.buttonname,self.devid, "now" ),50000)
    return """"""

class IDBuzzerMessage(resource.Resource):
  def __init__(self,mainhandler, devid):
    resource.Resource.__init__(self)
    #self.service = service
    self.devid = devid
    self.putChild("jquery.js", static.File("jquery.js"))
    self.putChild("webbuzzer", static.File("webbuzzer.html"))
    self.putChild("webteacher", static.File("webteacher.html"))
    csh = CometSetupHandler(mainhandler, devid)
    buttons = ["button1", "button2", "button3", "button4","teachernext"]
    for button in buttons:
      self.putChild(button, Button(button,devid))
    self.putChild("comet", csh)
      
    

  def render_GET(self, request):
    return """<html><head></head><body><div>Information about device ID X goes here</div></body></html>"""

class CometSetupHandler(resource.Resource):
  def __init__(self, mainhandler, devid):
    resource.Resource.__init__(self)
    self.mainhandler = mainhandler
    self.devid = devid

  def render_GET(self, request):
    self.mainhandler.appendCometId(request, self.devid)
    return webserver.NOT_DONE_YET
   
class MainBuzzerHandler(resource.Resource):
  def __init__(self,service):
    resource.Resource.__init__(self)
    self.service=service
    self.putChild("",self)
    self.idCometRequests = {} 


  def getChildWithDefault(self,devid,request):
    #name.split("/")
    
    print devid
    
    
    return IDBuzzerMessage(self, devid)

  def sendCometMessage(self, message):
    print "Sending Comet Messages"
    print len (self.idCometRequests)
    if message.devid in self.idCometRequests:
      
      requests = self.idCometRequests[message.devid]
      for r in requests:
        print "Updating"
        updateComet(r,message)


  def appendCometId(self,request, devid):
    if not (devid in self.idCometRequests):
      self.idCometRequests[devid] = []
    self.idCometRequests[devid].append(request)

class protocolGatewayService(service.Service):
  def __init__(self,multicastPort):
    self.multicastPort = multicastPort
    self.udpListeningPort = None
    self.httpListeningPort = None
    self.lproto = None
    self.reactor = None
  def startService(self):
    # called by application handling
    if not self.reactor:
      from twisted.internet import reactor
      self.reactor = reactor
    self.reactor.callWhenRunning(self.startStuff)
  def stopService(self):
    # called by application handling
    defers = []
    if self.udpListeningPort:
      defers.append(defer.maybeDeferred(self.udpListeningPort.loseConnection))
    if self.httpListeningPort:
      defers.append(defer.maybeDeferred(self.httpListeningPort.stopListening))
    return defer.DeferredList(defers)
  def startStuff(self):
    # UDP multicast stuff
    # Website
    mbh = MainBuzzerHandler(self)
    factory = webserver.Site(mbh)
    self.httpListeningPort = self.reactor.listenTCP(9001,factory)
    proto = multicastProtocol()
    proto.mainHandler = mbh
    self.udpListeningPort = self.reactor.listenMulticast(50001,proto,listenMultiple=True)
  def update_data(self,*args):
    self.data[:] = args
  def get_data(self):
    return self.data

application = service.Application('multicastGateway')
services = service.IServiceCollection(application)
s = protocolGatewayService(8000)
s.setServiceParent(services)

