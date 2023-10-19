from model.statistical_analysis import StatisticalAnalysis

def analyze(knowledgeGraph):
  return __calculate_histogram(knowledgeGraph)

def __top_of_histogram(knowledgeGraph):
  return 

def __calculate_histogram(knowledgeGraph):
  histogram=StatisticalAnalysis()
  for key, value in knowledgeGraph.get_graph().items():
    for i in range(9, len(value)):
      histogram.increment_value_of_link_of_token_and_position(key, value[i], i)
  return histogram
