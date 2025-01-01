from ..actions import file as FilesActions
from ..actions import text as TextActions

class Reading_YieldingActivity:

  def __init__(self, configuration, fileNames):
    self.fileNames = fileNames
    self.configuration = configuration

  def act(self):
    for fileName in self.fileNames:
      text = FilesActions.read_text_file(fileName)
      if self.configuration.commonWordReplacement != None: # Presence as an indicator of function.
        text = TextActions.remove_common_words(text, self.configuration.commonWordReplacement)
      yield text
