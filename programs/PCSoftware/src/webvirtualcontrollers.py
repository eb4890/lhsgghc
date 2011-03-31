import BaseHTTPServer
import SocketServer
import genericlib
import urlparse
import Cheetah
import shutil

PORT = 9001

class ControllerHandler (BaseHTTPServer.BaseHTTPRequestHandler):
   def do_GET(self):
     url = urlparse.urlparse (self.path)
     

     path = url.path
     pathsections = path.lstrip('/').split('/')
     thingid = pathsections[0]
     if len(pathsections) > 1 :
       if pathsections[1] == 'button':
       
         genericlib.broadcast("rawbuttonpress", "{0}:{1}:yesterday".format(pathsections[2], thingid), 50000)
         self.send_response(200)
         self.end_headers()
       elif pathsections[1] == 'startlesson':
         genericlib.broadcast("startlesson", "none",50000)
         self.send_response(200)
         self.end_headers()
       elif pathsections[1] =='nextquestion':
         genericlib.broadcast("nextquestion", "none", 50000)
         self.send_response(200)
       elif pathsections[1] in ['webbuzzer.html', "jquery.js"]:
         try:
           f = open(pathsections[1])
         except IOError, e:
           self.send_error(404, "File not found, this is pretty bad")  
         self.send_response (200)
         self.end_headers()
         shutil.copyfileobj(f, self.wfile)
         f.close()
       
     return
   def address_string(self):
     return str(self.client_address[0])
     




httpd = SocketServer.TCPServer(("", PORT), ControllerHandler)

httpd.serve_forever()
