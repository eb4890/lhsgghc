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
       
       genericlib.broadcast("rawbuttonpress", "{0}:11:yesterday".format(pathsections[1]), 50000)
       self.send_response(200)
       self.end_headers()
     elif pathsections[0] == 'startlesson':
       genericlib.broadcast("startlesson", "none",50000)
       self.send_response(200)
       self.end_headers()
     elif pathsections[0] =='nextquestion':
       genericlib.broadcast("nextquestion", "none", 50000)
       self.send_response(200)
        
     return
   def address_string(self):
     return str(self.client_address[0])
     




httpd = SocketServer.TCPServer(("", PORT), ControllerHandler)

httpd.serve_forever()
