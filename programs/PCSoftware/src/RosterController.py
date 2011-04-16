import messages
import network
import lessonparser as lp

class RosterController(MessageListener):
  def __init__(self, filename='', port):
    MessageListener.__init__(self, port)

    self.restart()
    if filename != '':
      self.loadrosterfile(filename)

  def restart(self, args=None):
    print "(Re)starting"
    self.started = False
    self.rosterpos = 0
    self.finished = False
    self.rosterlist = []
    self.rostermap = {}
    self.controller = {
      'startregistration' : self.startregistration,
      'rawbuttonpress': self.associate,
      'unregisterlast': self.unregisterlast,
      'rosterfile': self.rosterfile,
      'restart': self.restart,
    }

  def associate(self,args):
    print "In associate"

    print "after bp"
    try:
      if not (args["devid"] in self.rostermap) and not (self.finished) and self.started:

        currentstudent = self.rosterlist[self.rosterpos]
        self.rostermap [args["devid"]] = currentstudent
        ev = {
          'event':   'studentmapping',
          'devid':   args["devid"],
          'student': currentstudent,
        }
        messages.send(ev, 50000)
        self.rosterpos +=1
        if self.rosterpos >= len(self.rosterlist):
          self.finished = True
          self.rosterpos = len(self.rosterlist)

        print "Finished registration"
      else:
        print "%s already in rostermap" % args["devid"]

    except Exception, e:
      print rosterpos
      print "Malformed button event"
      print e

  def unregisterlast(self, args):
    self.rosterpos -=1

  def rosterfile (self, args):
    self.loadrosterfile (args)

  def loadrosterfile(self, filename):
    f = open(filename, "r")
    for line in f:
      self.rosterlist.append(line.strip())

  def startregistration(self,args):
    self.started = True

class LessonReader():
  def __setup__():
    pass


if __name__ == '__main__':
  rosterfilename = 'reg.txt'
  rc = RosterController(rosterfilename, 50001)
  rc.run()
