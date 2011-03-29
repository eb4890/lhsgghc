import BaseHTTPServer
import SocketServer
import genericlib
import urlparse

PORT = 9001

class ControllerHandler (BaseHTTPServer.BaseHTTPRequestHandler):
   def do_GET(self):
     url = urlparse.urlparse (self.path)
     

     path = url.path
     pathsections = path.lstrip('/').split('/')
     if pathsections[0] == 'button':
       
       genericlib.broadcast("rawbuttonpress", "test:{0}:11:yesterday".format(pathsections[1]), 50000)
       self.send_response(200)
       self.end_headers()
     elif pathsections[0] == 'start':
       genericlib.broadcast("startlesson", "none",50000)
       self.send_response(200)
       self.end_headers()
     return
   def address_string(self):
     return str(self.client_address[0])
     




httpd = SocketServer.TCPServer(("", PORT), ControllerHandler)

httpd.serve_forever()
