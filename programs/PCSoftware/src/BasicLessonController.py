import network
import messages
import json


class LessonController(MessageListener):
  def __init__(self, port):
    MessageListener.__init__(self, port)
    self.restart()

  def restart(self):
    self.lesson = ""
    self.lessonstarted = False
    self.handsets = []
    self.idtostudentmap = {"11":"Jimmy"}

    self.controller = {
      'rawbuttonpress': self.presetupbuttonpress,
      'startlesson': self.startlesson,
      'startregistration': self.startregistration,
      'studentmapping': self.studentmapping
    }

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
    self.controller["rawbuttonpress"] = self.livebuttonpress

  def startregistration(self):
    self.registrationstarted = True
    ev = { 'event': 'startregistration' }
    messages.send(ev, 50001)
    for h in self.handsets:
      messages.setlight(h, "#ffffff")

  def presetupbuttonpress(self,args):
    if args["button"] in ["button1", "button2", "button3", "button4"]:
      messages.send(args, 50001)
    elif args["button"] == "startregistration":
      print "Start registration"
      self.startregistration()
    elif args["button"] == "restart":
      ev = {'event': 'restart'}
      messages.send(ev, 50001)
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
    messages.send(ev, 50001)

if __name__ == '__main__':
  lc = LessonController(50000)
  lc.run()
