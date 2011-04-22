import network as net
import messages
import json
import fileops
import LessonParser as lp

class LessonController(net.MessageListener):
  def __init__(self, port):
    net.MessageListener.__init__(self, port)
    self.restart()

  def restart(self):
    self.questionnumber = 0
    self.lesson = None
    self.lessonfile = ""
    self.lessonresponsemap = []
    self.lessonstarted = False
    self.handsets = []
    self.displays = []
    self.idtostudentmap = {"11":"Jimmy"}
    self.registrationstarted = False
    self.controller = {
      'setlesson': self.setlesson,
      'rawbuttonpress': self.presetupbuttonpress,
      'startlesson': self.startlesson,
      'startregistration': self.startregistration,
      'studentmapping': self.studentmapping,
      'foundhandset': self.foundhandset,
      'founddisplay': self.founddisplay
    }
  
  def setlesson(self,args):
    self.lessonfile = args["lesson"]
    if self.lessonfile in fileops.getlessonlist():
      with open(args["lesson"]) as f:
        text = f.read()
        lp = lp.LessonParser()
        self.lesson = lp.parselesson(text)
        messages.send()
    else:
      messages.send({"event":"display","text":"Could not find lesson"}, 50001)
        
  def foundhandset(self, args):
    if not args["devid"] in self.handsets:
      self.handsets.append(args["devid"])

  def founddisplay(self,args):
    if not args["devid"] in self.displays:
      self.displays.append(args["devid"])

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
    if not self.registrationstarted:
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
    elif args["button"] == "startlesson":
      self.startlesson()
   
  def processbuttonnet(self,args):
    if (args["devid"] in idtostudentmap):
     
      student = idtostudentmap[args["devid"]]
      print student
      ev = {
        'event':    'processedbuttonpress',
        'student':  student,
        'button':   args['button'],
        'realtime': args['rawtime']
      }
    else:
      ev = {
        'event': 'anonbuttonpress',
        'button': args['button'],   
        'realtime': args['rawtime']
      }
    messages.send(ev, 50001)

  def processbutton(self,args):
    self.lessonresponsemap

  def nextquestion(self, args):
    self.lessonresponsemap.append({})
    self.questionnumber = self.questionnumber + 1
    for d in self.displays:
      ev = {
       "event":"nextquestion",
       "question":"",
       "devid": d
      }
      messages.send(ev, 50001)

  def livebuttonpress(self,args):
    print "Pressingbutton"
    if (args["buttoname"] in ["button" + str(n) for n in range(1,4)]):
      self.processbutton()
    elif args["button"] == "teachernext":
      self.nextquestion():
         
    #messages.send(ev, 50001)

if __name__ == '__main__':
  lc = LessonController(50000)
  lc.run()
