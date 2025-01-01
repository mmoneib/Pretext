from ..actions import token as TokenActions

class Statistics_ProceduralActivity:

  def __init__(self, tokenGraph):
    self.tokenGraph = tokenGraph
    self.meta = {} # A backdoor too add values and/or keys which are not part of the main output.

  def act(self):
    self.tokenScore = TokenActions.calculate_histograms(self.tokenGraph)
    self.tokenChoice = TokenActions.top_of_histogram(self.tokenGraph)
    return self # For chaining.

  def output(self):
    return self.tokenChoice

  def get_meta_output(self):
    return self.meta
