from ..actions import token as TokenActions

class StatisticsProcedural:

  def __init__(self, tokenGraph):
    self.tokenGraph = tokenGraph

  def process(self):
    self.tokenScore = TokenActions.calculate_histograms(self.tokenGraph)
    self.tokenChoice = TokenActions.top_of_histogram(self.tokenGraph)
    return self # For chaining.

  def output(self):
    return self.tokenChoice

