import re

possibleanswerdemarcators = '[a-zA-Z0-9]*[\]\)\}\.\:]'

re.DOTALL = True

#This is a monadic style bit of code. But what to be done.

numbering = r'\(?(\d+|i+|I+|[A-Z])([\.\)\:\,])'

# - dashes


def parsetitle(text):
  lines = text.split('\n')
  for l in lines:
    if re.match(r'^(\w)*(Q|%s)' % numbering ,l):
      print 'Matched %s' %l
  #matches =  re.match('([^Q.])*Q', text)
  #print matches.group(0)
  return

def parseanswer(text):

  return

def parsequestion(text):
  return

def parsequestiontotal(text):
  return


def parselesson(text):

  (title,rest) = parsetitle (text)
  questions = []
  while (rest!=''):
    rest, question = parsequestiontotal(rest)
    questions.append (question)

  return {'title': title, 'questions': question}


parsetitle('asasjlaj\nIII.dladj\n\\nasad\nQ\n1)\n|n\n(\)')
