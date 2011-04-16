import network
import messages
import json


class LessonController():
  def __init__(self):
    self.restart()
  def studentmapping(self, args):
    try:
      self.idtostudentmap[args["devid"]] = args["student"]
      messages.setlight(args["devid"], "#000000")
    except Exception,e :
      print "Incorrect message format"
      print e

  def startlesson(self, args):
    self.lessonstarted = True
    print "Changing eventmap"
    self.eventmap["rawbuttonpress"] = self.livebuttonpress

  def startregister(self):
    self.registrationstarted = True
    ev = { 'event': 'startregistration' }
    network.broadcast(ev, 50001)
    for h in self.handsets:
      messages.setlight(h, "#ffffff")

  def presetupbuttonpress(self,args):
    if args["button"] in ["button1", "button2", "button3", "button4"]:
      network.broadcast(args, 50001)
    elif args["button"] == "startregistration":
      print "Start registration"
      self.startregister()
    elif args["button"] == "restart":
      ev = {'event': 'restart'}
      network.broadcast(ev, 50001)
      self.restart()

  def livebuttonpress(self,args):
    print "Pressingbutton"

    student = idtostudentmap[args["devid"]]
    print student
    ev = {
      'event':    'processedbuttonpress',
      'student':  student,
      'button':   args['button'],
      'realtime': args['rawtime']
    }
    network.broadcast(ev, 50001)

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

lc = LessonController()

network.listen(lc.eventmap, 50000)
