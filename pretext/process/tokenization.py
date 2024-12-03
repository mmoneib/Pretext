from ..actions import text as TextActions
import time

class TokenizationParallel:

  def __init__(self, configuration, text):
    self.charsTokenizationSteps=configuration.charsTokenizationSteps
    self.wordsTokenizationSteps=configuration.wordsTokenizationSteps
    self.numberOfTokenizationThreads=configuration.numberOfTokenizationThreads
    self.isBlocking = True
    self.text = text

  def process(self):
    self.tokens=[]
    if self.charsTokenizationSteps > 0:
      for i in range(0, self.charsTokenizationSteps):
        self.tokens.extend(TextActions.tokenize_by_chars(self.text, i+1))
    if self.wordsTokenizationSteps > 0:
      for i in range(0, self.wordsTokenizationSteps):
        self.tokens.extend(TextActions.tokenize_by_words(self.text, i+1))
    self.isComplete = True
    #print(self.tokens)
    return self # For chaining.

  def output(self):
    if self.isBlocking:
      return self.__output_complete()
    else:
      return self.__output_maybe_incomplete()

  def __output_complete(self): # Busy waiting until output is available.
    while self.isComplete == False:
      time.sleep(1)  
    return self.tokens

  def __output_maybe_incomplete(self): # Unguaranteed ouptut in case of multi-threads.
    return self.tokens
