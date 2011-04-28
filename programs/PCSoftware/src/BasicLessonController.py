import network as net
import messages
import json
import fileops
import LessonParser as LP

def getbuttonlist():
  return (["button1", "button2", "button3", "button4"])
  #Alternately ["button" + str(n) for n in range(1,4)]

class LessonController(net.MessageListener):
  def __init__(self, port):
    net.MessageListener.__init__(self, port)
    self.restart()

  def restart(self):
    self.questionnumber = 0
    self.lesson = None
    self.lessonfile = ""
    self.lessonresponsemap = []
    self.questionresponsemap = {}
    self.lessonstarted = False
    self.handsets = []
    self.displays = []
    self.idtostudentmap = {} 
    self.registrationstarted = False
    self.controller = {
      'setlesson': self.setlesson,
      'rawbuttonpress': self.presetupbuttonpress,
      #'startlesson': self.startlesson,
      'startregistration': self.startregistration,
      'studentmapping': self.studentmapping,
      'foundhandset': self.foundhandset,
      'founddisplay': self.founddisplay
    }
  
  def senddisplaymsg(self, text):
    for d in self.displays:
      messages.send({"event":"display", "text": text, "devid":d}, 50001)

  def setlesson(self,args):
    self.lessonfile = args["lesson"]
    print self.lessonfile
    print repr (fileops.getlessonlist())
    if self.lessonfile in fileops.getlessonlist():
      with open("./admin/lessons/"+self.lessonfile) as f:
        text = f.read()
        lp = LP.LessonParser()
        self.lesson = lp.parselesson(text)
        self.senddisplaymsg(self.lesson["title"]) 
    else:
      self.senddisplaymsg ("Could not find lesson") 
        
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

  def startlesson(self): #, args
    
    if self.lesson !=None: 
      self.lessonstarted = True
      print "Changing eventmap"
      self.controller["rawbuttonpress"] = self.livebuttonpress
      self.nextquestion()
    else:
      self.senddisplaymsg("Lesson not selected yet")
      # Make infinite mode here

  def startregistration(self):
    self.registrationstarted = True
    ev = { 'event': 'startregistration' }
    messages.send(ev, 50001)
    for h in self.handsets:
      messages.setlight(h, "#ffffff")
    

  def presetupbuttonpress(self,args):
    if args["button"] in getbuttonlist():
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
    if (args["devid"] in self.idtostudentmap):
     
      student = self.idtostudentmap[args["devid"]]
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
    #Need to make sure that anonid cannot be a devid. Else things will get confused. The perfect is the enemy of the done, though.
    anonid = "anon" + args["button"]
    if args[""] 
    elif args["devid"] in self.idtostudentmap and args["devid"] not in self.questionresponsemap:
      self.questionresponsemap[args["devid"]] = (args ["button"], args)
    elif anonid in self.questionresponsemap:
      self.questionresponsemap[anonid ] +=1
    else:
      self.questionresponsemap[anonid] = 1
  

   
 
  def sendreport(self):
    text = "<table><tr><th>Question</th>"
    anontext = "<H1>Anonymous Answers<H1>" + text
    for (k, s) in self.idtostudentmap.items():
      text += "<th>%s</th>" % s
    qcount = 0

    text += "</tr>"
    for b in getbuttonlist():
      anontext += "<th>%s</th>" % b
    anontext += "<tr>" 

    for q in self.lessonresponsemap:
      (qtext, ls) = self.lesson["questions"][qcount]
      questiontext = "<tr><td>%s</td>" % qtext
      text+= questiontext
      anontext += questiontext
      for (k, s) in self.idtostudentmap.items():
        if k in q:
          (devid, args) =  q[k]
          ans = args["button"]
        else: 
          ans = "No answer"
        text +="<td>%s</td>" % ans
      for b in getbuttonlist():
        anonbutton = "anon" +b 
        if anonbutton in q:
          acount  = q["anon"+b]
        else: 
          acount  = 0
        anontext += "<td>%s</td>" % acount
      text+="</tr>"
      anontext+="</tr>"
      qcount +=1

    text += "</table>"
    anontext+= "</table>"
    

    self.senddisplaymsg(text + anontext)

  def nextquestion(self):
    
    if self.questionnumber != 0:
      self.lessonresponsemap.append(self.questionresponsemap)
      self.questionresponsemap = {}
    print "lesson response map is %d long" % len(self.lessonresponsemap)
    if self.questionnumber < len (self.lesson["questions"]):
      (q, ls) = self.lesson["questions"][self.questionnumber]
      q += "<ul>"
      for l in ls:
        q += "<li>" + l + "</li>"
      q+= "</ul>"
      self.senddisplaymsg(q)
      self.questionnumber = self.questionnumber + 1
    else:
      self.sendreport()
  def livebuttonpress(self,args):
    print "Pressingbutton"
    if (args["button"] in getbuttonlist()):
      self.processbutton(args)
    elif args["button"] == "teachernext":
      self.nextquestion()
         
    #messages.send(ev, 50001)

if __name__ == '__main__':
  lc = LessonController(50000)
  lc.run()
