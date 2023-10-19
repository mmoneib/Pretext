class KnowledgeGraph:
  def __init__(self):
    self.graph={}

  def link(self, token, correspondingTokens):
    self.graph[token]=correspondingTokens

  def getLinks(self, token):
    links=[]
    for key, value in self.graph.items():
      if key == token:
        links+=value
    return links

  def get_graph(self):
    return self.graph
