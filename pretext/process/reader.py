class ReaderYieldingProcess:

  def __init__(self, fileNames):
    self.fileNames=fileNames

  def start(self):
    for fileName in self.fileNames:
      yield self.__openText(fileName)

  def __openText(self, fileName):
    with open(fileName, 'r') as f:
      data = f.read()
      return data 
