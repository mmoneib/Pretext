from ..actions import token as TokenActions
import time

class Modeling_ParallelActivity:

  def __init__(self, tokens, tokenGraph):
    self.tokens = tokens
    self.tokenGraph = tokenGraph
    self.isBlocking = True

  def act(self):
    self.tokenGraph = TokenActions.model_by_next(1, self.tokens, self.tokenGraph)
    self.isComplete = True
    return self # For chaining.

  def output(self):
    if self.isBlocking:
      return self.__output_complete()
    else:
      return self.__output_maybe_incomplete()

  def __output_complete(self): # Busy waiting until output is available.
    while self.isComplete == False:
      time.sleep(1)  
    return self.tokenGraph

  def __output_maybe_incomplete(self): # Unguaranteed ouptut in case of multu-threads.
    return self.tokenGraph
