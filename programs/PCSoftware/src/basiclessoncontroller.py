import genericlib as gl



class LessonController():
  def __init__(self):
    self.lesson = ""
    self.lessonstarted = False
    self.idtostudentmap = {"11":"Jimmy"}
    self.eventmap = {"rawbuttonpress": self.presetupbuttonpress,
                     "startlesson": self.startlesson,
                     "studentmapping": self.studentmapping
                    }
  def studentmapping(self, args):
    assoc = gl.Association(string = args)
    self.idtostudentmap[assoc.key] = assoc.value
  
  def startlesson(self, args):
    self.lessonstarted = True
    print "Changing eventmap"
    self.eventmap["rawbuttonpress"] = self.livebuttonpress
    #self.eventmap["rawbuttonpress"]("test:1:11:yesterday")
  
  def presetupbuttonpress(self,args):
    gl.broadcast("rawbuttonpress", args, 50001)

  def livebuttonpress(self,args):
    bp = gl.ButtonPress(args)
    print "Pressingbutton"
    
    student= idtostudentmap[bp.buzzerid] 
    print student
    #print "Student {1}".format(student)
    gl.broadcast("parsedbuttonpress", ":".join([student,bp.button,bp.timestamp]), 50001)

def test(args):
  print args

lc = LessonController()

gl.listen(lc.eventmap, 50000)
