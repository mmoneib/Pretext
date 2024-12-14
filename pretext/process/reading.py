from ..actions import file as FilesActions

class ReadingYieldingProcess:

  def __init__(self, fileNames):
    self.fileNames=fileNames

  def process(self):
    for fileName in self.fileNames:
      yield FilesActions.read_text_file(fileName)
