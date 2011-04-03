import genericlib as gl

class RegisterController():
  def __init__(self, filename= ""):
    self.registerpos = 0
    self.finished = False
    self.registerlist = []
    self.registermap = {}  
    self.eventmap= {
                  "rawbuttonpress": self.associate, 
                  "unregisterlast": self.unregisterlast,
                  "registerfile": self.registerfile
                  }   
    if filename != "":
      self.loadregfile (filename)
  def associate(self,args):
    print "In associate"
    bp = gl.ButtonPress(args)
    print "after bp"
    if not (bp.buzzerid in self.registermap) and not (self.finished):
      currentstudent = self.registerlist[self.registerpos]
      self.registermap [bp.buzzerid] = currentstudent
      gl.broadcast("studentmapping",gl.Association(key = bp.buzzerid,value =currentstudent).toText(),50000)
      self.registerpos +=1
      if self.registerpos == len (self.registermap):
        self.finished = True
  

  def unregisterlast(self, args):
    self.registerpos -=1

  def registerfile (self, args):
    self.loadregfile (args)
  def loadregfile(self, filename):
    f = open(filename, "r")
    for line in f:
      self.registerlist.append(line.strip())
    
registerfilename = "reg.txt"
rc = RegisterController(registerfilename)
gl.listen(rc.eventmap, 50001)
