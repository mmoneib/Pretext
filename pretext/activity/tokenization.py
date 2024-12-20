from ..actions import text as TextActions
import time

class Tokenization_ParallelActivity:

  def __init__(self, configuration, text):
    self.charsTokenizationSteps=configuration.charsTokenizationSteps
    self.wordsTokenizationSteps=configuration.wordsTokenizationSteps
    self.numberOfTokenizationThreads=configuration.numberOfTokenizationThreads
    self.isBlocking = True # Should be allowed to be false if partial outputs are to be tolerated. (Un)blocking mechanism is necessary for parallel computations.
    self.text = text

  def act(self):
    self.tokens=[]
    if len(self.charsTokenizationSteps) > 0:
      for i in range(0, len(self.charsTokenizationSteps)):
        self.tokens.extend(TextActions.tokenize_by_chars(self.text, i+1))
    if len(self.wordsTokenizationSteps) > 0:
      for i in range(0, len(self.wordsTokenizationSteps)):
        self.tokens.extend(TextActions.tokenize_by_words(self.text, i+1))
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
