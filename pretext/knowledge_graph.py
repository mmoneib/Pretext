class KnowledgeGraph:
  def __init__(self):
    self.graph=[]

  def link(self, token, otherToken):
    self.graph+=(token, otherToken)
