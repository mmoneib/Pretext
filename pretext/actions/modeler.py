from model.knowledge_graph import KnowledgeGraph

def model_by_next(tokens, knowledgeGraph):
  for i in range(0, len(tokens)-1):
    knowledgeGraph.link(tokens[i], [tokens[i+1]])
  knowledgeGraph.link(tokens[i+1], [""])
  return knowledgeGraph
  
