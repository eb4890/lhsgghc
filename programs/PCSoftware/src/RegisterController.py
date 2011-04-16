import genericlib as gl
import lessonparser as lp
class RegisterController():
  def __init__(self, filename= ""):
    self.restart(None)
    if filename != "":
      self.loadregfile (filename)
  
  def restart(self,args):
    print "(Re)starting"
    self.started = False
    self.registerpos = 0
    self.finished = False
    self.registerlist = []
    self.registermap = {}  
    self.eventmap= { "startregistration" : self.startregistration,
                  "rawbuttonpress": self.associate, 
                  "unregisterlast": self.unregisterlast,
                  "registerfile": self.registerfile,
 	          "restart": self.restart
                  }   

  def associate(self,args):
    print "In associate"
    #bp = gl.ButtonPress(args)
    
    print "after bp"
    try: 
      if not (args["devid"] in self.registermap) and not (self.finished) and self.started:
       
        currentstudent = self.registerlist[self.registerpos]
        self.registermap [args["devid"]] = currentstudent
        gl.broadcast("""{"event": "studentmapping", "devid":"%s" , "student": "%s" }""" % (args["devid"], currentstudent),50000)
        self.registerpos +=1
        if self.registerpos >= len (self.registerlist):
          self.finished = True
          self.registerpos = len(self.registerlist)
	  print "Finished registration"
      else:
        print "%s already in registermap" % args["devid"]
    except Exception, e:
      print regusterois
      print "Malformed button event" 
      print e 

  def unregisterlast(self, args):
    self.registerpos -=1

  def registerfile (self, args):
    self.loadregfile (args)
  def loadregfile(self, filename):
    f = open(filename, "r")
    for line in f:
      self.registerlist.append(line.strip())
  
  def startregistration(self,args):
    self.started = True

class LessonReader():
  def __setup__():
    pass
    
registerfilename = "reg.txt"
rc = RegisterController(registerfilename)
gl.listen(rc.eventmap, 50001)
