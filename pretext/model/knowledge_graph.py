## List(token,List(linkedToken))
class KnowledgeGraph:
  def __init__(self):
    self.graph=[]

  def link(self, token, correspondingTokens):
    self.graph.append((token, correspondingTokens))

  def getLinks(self, token):
    links=[]
    for tokenAndLinks in self.graph:
      if tokenAndLinks[0] == token:
        links.append(tokenAndLinks[1])
    return links

  def get_graph(self):
    print(self.graph)
    return self.graph
