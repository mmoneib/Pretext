from ..actions import file as FilesActions

class Reading_YieldingActivity:

  def __init__(self, fileNames):
    self.fileNames=fileNames

  def act(self):
    for fileName in self.fileNames:
      yield FilesActions.read_text_file(fileName)
