def getlessonlist():
  dirs = os.walk("./lessons")
  lessons = []
  for root, d, fs in dirs:     
    fullfs = [root +"/"+ f for f in fs]
    lessons.extend(fullfs)
  return lessons
