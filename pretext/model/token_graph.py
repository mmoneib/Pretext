## List(Tuple(token,List(linkedToken)))
class TokenGraph:
  def __init__(self):
    self.graph=[]

  def link(self, token, correspondingTokens):
    self.graph.append((token, correspondingTokens))

  def get_links(self, token):
    links=[]
    for tokenAndLinks in self.graph:
      if tokenAndLinks[0] == token:
        links.append(tokenAndLinks[1])
    return links

  def get_graph(self):
    self.__print_graph()
    return self.graph

  def __print_graph(self):
    print("Graph: ", self.graph)

  def __pretty_print_graph(self):
    print("Graph:")
    for item in self.graph:
      print(item)
