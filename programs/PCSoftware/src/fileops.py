import os

def getlessonlist():
  dirs = os.walk(os.path.expanduser("~/.buzzers/lessons"))
#"/home/loadquo/files/lhsgghc/Programs/PCSoftware/src/admin/lessons")
  lessons = []
  for root, d, fs in dirs:     
    fullfs = [root +"/"+ f for f in fs]
    lessons.extend(fs)
  return lessons
