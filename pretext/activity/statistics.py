from ..actions import token as TokenActions

class Statistics_ProceduralActivity:

  def __init__(self, tokenGraph):
    self.tokenGraph = tokenGraph

  def act(self):
    self.tokenScore = TokenActions.calculate_histograms(self.tokenGraph)
    self.tokenChoice = TokenActions.top_of_histogram(self.tokenGraph)
    return self # For chaining.

  def output(self):
    return self.tokenChoice

