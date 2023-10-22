def read(fileNames):
  for fileName in fileNames:
    yield __openText(fileName)

def __openText(fileName):
  with open(fileName, 'r') as f:
    data = f.read()
    return data 
