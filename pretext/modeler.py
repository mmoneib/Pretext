from knowledge_graph import KnowledgeGraph

def model(tokens, knowledgeGraph):
  return __model_by_next(tokens, knowledgeGraph)

def __model_by_next(tokens, knowledgeGraph):
  for i in range(0, len(tokens)-1):
    knowledgeGraph.link(tokens[i], tokens[i+1])
  knowledgeGraph.link(i+1, None)
  return knowledgeGraph
  
