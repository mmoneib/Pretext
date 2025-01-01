from ..actions import text as TextActions
from ..actions import token as TokenActions
import time

class Tokenization_ParallelActivity:

  def __init__(self, configuration, text):
    self.charsTokenizationSteps=configuration.charsTokenizationSteps
    self.wordsTokenizationSteps=configuration.wordsTokenizationSteps
    self.tokenizationSeparator=configuration.tokenizationSeparator
    self.numberOfTokenizationThreads=configuration.numberOfTokenizationThreads
    self.isBlocking = True # Should be allowed to be false if partial outputs are to be tolerated. (Un)blocking mechanism is necessary for parallel computations.
    self.text = text
    self.isComplete = False

  def act(self):
    self.isComplete = True
    self.tokens=[]
    if len(self.charsTokenizationSteps) > 0:
      for i in self.charsTokenizationSteps:
        self.tokens.extend(TextActions.tokenize_by_chars(self.text, i))
        TokenActions.append_tokenization_separator(self.tokens, self.tokenizationSeparator)
    if len(self.wordsTokenizationSteps) > 0:
      for i in self.wordsTokenizationSteps:
        self.tokens.extend(TextActions.tokenize_by_words(self.text, i))
        TokenActions.append_tokenization_separator(self.tokens, self.tokenizationSeparator)
    self.isComplete = True
    #print(self.tokens)
    return self # For chaining with output.

  def output(self, sleepBeforeFirstAttemptInSeconds=None, sleepAfterFirstAttemptInSeconds=1):
    if sleepBeforeFirstAttemptInSeconds is not None:
      time.sleep(sleepBeforeFirstAttemptInSeconds) # Useful for asynchronous calls outside the main thread.
    if self.isBlocking:
      return self.__output_complete(sleepAfterFirstAttemptInSeconds)
    else:
      return self.__output_maybe_incomplete()

  def __output_complete(self, sleepAfterFirstAttemptInSeconds): # Busy waiting until output is available.
    while self.isComplete == False:
      time.sleep(sleepAfterFirstAttemptInSeconds)
    return self.tokens

  def __output_maybe_incomplete(self): # Unguaranteed ouptut in case of multi-threads.
    return self.tokens

def get_task_output(task): # Required as a global because map(...) of ProcessPoolExecutor doesn't accept local functions (like lambda).
  return task.act().output()
