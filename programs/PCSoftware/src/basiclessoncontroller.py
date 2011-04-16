import genericlib as gl
import json


class LessonController():
  def __init__(self):
    self.restart()
  def studentmapping(self, args):
    #assoc = gl.Association(string = args)
    try: 
      self.idtostudentmap[args["devid"]] = args["student"]
      gl.setlight(args["devid"],"#000000")
      #gl.broadcast("""{"event": "setlight" , "devid":"%s", "state": "%s"}""" % (args["devid"], "off") , 50001)
    except Exception,e :
      print "Incorrect message format"
      print e
    #gl.broadcast ("{'event':'association', 'type': 'studentid', 'key':'%s', 'value':'%s'}" % (assoc.key, assoc.value))
    #When a student mapping is made we need to turn off a light 

  def startlesson(self, args):
    self.lessonstarted = True
    print "Changing eventmap"
    self.eventmap["rawbuttonpress"] = self.livebuttonpress
    #self.eventmap["rawbuttonpress"]("test:1:11:yesterday")
  

  def startregister(self):
    self.registrationstarted = True  
    gl.broadcast ("""{"event": "startregistration"} """, 50001)
    for h in self.handsets:
      setlight(h, "#ffffff")
   
     
  def presetupbuttonpress(self,args):
    if args["button"] in ["button1", "button2", "button3", "button4"]:
      #if (self.registrationstarted)
      
      gl.broadcast(json.dumps(args), 50001)
    elif args["button"] == "startregistration":
      print "Start registration"
      self.startregister()
    elif args["button"] == "restart":
      gl.broadcast("""{"event": "restart"}""",50001)
      self.restart() 
  def livebuttonpress(self,args):
    #bp = gl.ButtonPress(args):
    print "Pressingbutton"
    
    student= idtostudentmap[args["devid"]] 
    print student
    #print "Student {1}".format(student)
    gl.broadcast("""{"event":"processedbuttonpress" , "student":"%s", "button": "%s", "realtime" : "%s"}""" % (student, args["button"], args["rawtime"]), 50001)

  def restart(self):
    self.lesson = ""
    self.lessonstarted = False
    self.handsets = []
    self.idtostudentmap = {"11":"Jimmy"}
    self.eventmap = {
                     "rawbuttonpress": self.presetupbuttonpress,
                     "startlesson": self.startlesson,
                     "startregister": self.startregister, 
                     "studentmapping": self.studentmapping
                    }
    
def test(args):
  print args

lc = LessonController()

gl.listen(lc.eventmap, 50000)
