from actions import token as TokenActions
import time

class ModelingParallel:

  def __init__(self, tokens, tokenGraph):
    self.tokens = tokens
    self.tokenGraph = tokenGraph

  def process(self):
    self.tokenGraph = TokenActions.modelByNext(self.tokens, self.tokenGraph)
    isComplete = True
    return self # For chaining.

  def output_complete(self): # Busy waiting until output is available.
    while isComplete == False:
      time.sleep(1)  
    return self.tokenGraph

  def output_maybe_incomplete(self): # Unguaranteed ouptut in case of multu-threads.
    return self.tokenGraph
