from ..actions import files as FilesActions

class ReadingYieldingProcess:

  def __init__(self, fileNames):
    self.fileNames=fileNames

  def process(self):
    for fileName in self.fileNames:
      yield FilesActions.openTextFileAsReadOnly(fileName)
