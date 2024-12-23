from ..actions import token as TokenActions
import time

class Modeling_ParallelActivity:

  def __init__(self, configuration, tokens, tokenGraph):
    self.tokenizationSeparator = configuration.tokenizationSeparator
    self.tokens = tokens
    self.tokenGraph = tokenGraph
    self.isBlocking = True
    self.isComplete = False

  def act(self):
    self.tokenGraph = TokenActions.model_by_next(1, self.tokens, self.tokenGraph, self.tokenizationSeparator) # TODO Make it configurable.
    self.isComplete = True
    return self # For chaining.

  def output(self):
    if self.isBlocking:
      return self.__output_complete()
    else:
      return self.__output_maybe_incomplete()

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
    return self.tokenGraph

  def __output_maybe_incomplete(self): # Unguaranteed ouptut in case of multi-threads.
    return self.tokenGraph

def get_task_output(task): # Required as a global because map(...) of ProcessPoolExecutor doesn't accept local functions (like lambda).
  return task.act().output()
