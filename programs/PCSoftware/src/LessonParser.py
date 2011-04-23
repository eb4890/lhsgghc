import re

possibleanswerdemarcators = r'[a-zA-Z0-9]*[\]\)\}\.\:]'

re.DOTALL = True

#This is a monadic style bit of code. But what to be done.

x = re.match("Q(uestion)?", "Question")

for i in x.groups():
  print i


question = r"Q((uestion)|\.|:)?"
answer = r"A((nswer)|\.|:)?"
#answer = r"a|A(\.)?|Answer"


#prenumber = r'(\s)*\(?(%s)?(\s*)%s([\.\)\:\,\s\b].*)$'
prenumber = r'(\s)*\(?(%s)?\s*%s($|([\.\s\:\,\)].*$))'
numberings = [
r"\d+",
r"i+",
r"I+",
r"[A-Z]",
r"[a-z]"
] 

# - dashes
class LessonParser():
  
  def __init__(self):
    self.questions = []
    self.rest = []
    self.majorre = ""
    self.minorre = ""
  
  def findmajorstart(self, line):
    matched = False
    for n in numberings:

      match =  re.match(prenumber % (question, n), line) 
      if match:
        
        self.majorre = n  
        matched = True
     #   for g in match.groups():
          #print "found group %s" % g 
        print "Found major marker %s" % n
    return matched 
 
  def findminorstart(self, line):
    matched = False
    print "Line = %s" % line
    for n in numberings:
      if re.match (prenumber % (answer, n), line):
        self.minorre = n
        matched = True
        print "Found minor marker %s" % n
    return matched

  def parsetitle(self, text):
    lines = text.split('\n')
    title  = ""
    rest = []
    matched = False
    for l in lines:
      if not matched:
        matched  = self.findmajorstart(l)
        #matched = re.match(r'^(\w)*(Q|Question|%s)*' % numbering ,l)
        #print 'Title %s' %l
        if not matched:
          title = "\n".join([title,l])
        else:
          self.rest.append(l)
      else:
        self.rest.append( l)
        #print "appending %s" % l
    self.title = title
      
  #matches =  re.match('([^Q.])*Q', text)
  #print matches.group(0)

  def parseanswer(self):
    answer = self.rest[0]
    self.rest = self.rest[1:]
    count = 0
    #print "First line %s" % self.rest[0] 
    for l in self.rest:
      if ((not self.questionnext(l)) and (not self.newanswer(l))):  
        answer = "\n".join([answer, l])
        #print "answer %s" % answer
      else:
        print "Count = %d, self.rest = %d"% (count, len(self.rest))        
        if count <= len (self.rest):
         
          self.rest = self.rest[(count):]  
        else:
          self.rest = []
        #print repr(self.rest)
        return answer

      count = count +1
      print count
    self.rest = []
    return answer

  def parsequestion(self, text):
    if self.rest != []: 
      question = self.rest[0]
      
      print self.rest[0]
      self.rest = self.rest[1:]
    matched = False
    count = 0
    #print "In minorre find"
    for l in self.rest:
      print count
      if self.minorre == "":
        if self.findminorstart(l):
          self.rest = self.rest[count:]
          return question      
        else:
          question = "\n".join([question, l ])
      elif self.newanswer(l):
        self.rest = self.rest[count:]
        print repr (self.rest)
        return question
      else:
        question = "\n".join([question, l ])
        count = count + 1
    self.rest = []
    return question
   
  def questionnext(self, l):
    ret = False
      
      #print "matching %s" % l
    if re.match ( prenumber %(question, self.majorre), l ):    
      ret =  True
 
    return ret
  
  def newanswer(self, l):
    ret = False
    if re.match( prenumber % (answer, self.minorre), l):
      ret = True
    return ret        
  
  def parsequestiontotal(self, text):
    question = self.parsequestion(text)
    answers = []
    #print "pqtb %s" % self.rest[0]
    notquestionnext = True
    while( notquestionnext and self.rest != []):
      a = self.parseanswer()
      #print "pqt"
      answers.append(a)
      #print repr (a)
      #print repr (self.rest)
      #if self.rest != []:
       
       #  self.rest = self.rest[1:]
      if self.rest != []:
        notquestionnext = not self.questionnext(self.rest[0]) 
    return (question, answers)    

 
  def parselesson(self, text):

    self.parsetitle (text)
    questions = []
    #print repr(self.rest)
    while (self.rest!=[]):
      #print repr(self.rest)
      question = self.parsequestiontotal(self.rest)
      questions.append (question)

    return {'title': self.title, 'questions': questions}


n = LessonParser()
with open("admin/lessons/lesson1") as f:
  text = f.read()
  print text
  dicto = n.parselesson(text)
  print "Title = %s" % dicto['title']
  for (q, answers) in dicto['questions']:
    print "Question found: '%s' with answers:" % q
    for a in answers:
      print "\tAnswer found '%s'" % a 
#print "leftover = %s" % repr(dicto['questions']) 
