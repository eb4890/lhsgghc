from twisted.internet import protocol, defer
from twisted.application import service
from twisted.python import log
from twisted.web import resource, server as webserver

import struct

multicastgroup = "224.0.0.1"

class multicastProtocol(protocol.DatagramProtocol):
  def startProtocol(self):
    self.transport.joinGroup(multicastgroup)
    #self.transport.connect(self.service.multicastHost,self.service.multicastPort)
    #self.sendMessage("Send me data")
  def stopProtocol(self):
    return
  def datagramReceived(self,datagram,addr):
    try:
      event, data = datagram.split("\n")
      print "Found" + event + data
    except Exception as err:
      log.err()
      return
 # def sendMessage(self,message):
  # self.transport.write(message)

#class 

class IDBuzzerMessage(resource.Resource):
  def __init__(self,service,thisid):
    resource.Resource.__init__(self)
    self.service = service
    self.thisid = thisid
    self.putChild("jquery.js", File("jquery.js"))
    self.putChild("webbuzzer", File("webbuzzer.html"))
    self.putChild("webteacher", File("webteacher.html"))
  

class BuzzerMessageHandler(resource.Resource):
  def __init__(self,service):
    resource.Resource.__init__(self)
    self.service=service
    self.putChild("",self)
  
  def getChild(self,name,request):
    #name.split("/")
    print name
    return self

  def render_GET(self,request):
    data = "\n".join(["<li>%s</li>" % x for x in self.service.get_data()])
    return """<html><head><title>multicast Data</title>
      <body><h1>Data</h1><ul>
      %s
      </ul></body></html>""" % (data,)

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
    proto = multicastProtocol()
    proto.service = self
    self.udpListeningPort = self.reactor.listenMulticast(50000,proto,listenMultiple=True)
    # Website
    factory = webserver.Site(BuzzerMessageHandler(self))
    self.httpListeningPort = self.reactor.listenTCP(9001,factory)
  def update_data(self,*args):
    self.data[:] = args
  def get_data(self):
    return self.data

application = service.Application('multicastGateway')
services = service.IServiceCollection(application)
s = protocolGatewayService(8000)
s.setServiceParent(services)

