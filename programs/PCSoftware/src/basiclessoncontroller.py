import genericlib

class ButtonPress (): 
   def __init__(self, args="", dictionary ={}):
     if (args != ""):
       self.origin, self.button, self.buzzerid, self.timestamp = args.split(':')
     elif dictionary != {}:
       self.origin = dictionary[origin]
 
       self.buzzerid = dictionary[buzzerid]
       self.timestamp = dictionary[timestamp]
       self.button = dictionary[button]

class LessonController():
  def __init__(self):
    self.lesson = ""
    self.lessonstarted = False
    self.idtostudentmaps = {}
    self.idtostudentmaps["test"] = {"11":"Jimmy"}
    self.eventmap = {"rawbuttonpress": self.presetupbuttonpress,
                     "startlesson": self.startlesson
                    }

  
  def startlesson(self, args):
    self.lessonstarted = True
    print "Changing eventmap"
    self.eventmap["rawbuttonpress"] = self.livebuttonpress
    #self.eventmap["rawbuttonpress"]("test:1:11:yesterday")
  
  def presetupbuttonpress(self,args):
    genericlib.broadcast("rawbuttonpress", args, 50001)

  def livebuttonpress(self,args):
    bp = ButtonPress(args)
    print "Pressingbutton"
    print bp.origin
    idtostudent = self.idtostudentmaps[bp.origin]
    student= idtostudent[bp.buzzerid] 
    print student
    #print "Student {1}".format(student)
    genericlib.broadcast("parsedbuttonpress", ":".join([student,bp.button,bp.timestamp]), 50001)

def test(args):
  print args

lc = LessonController()

genericlib.listen(lc.eventmap, 50000)
