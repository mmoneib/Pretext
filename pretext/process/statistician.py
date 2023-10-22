from model.statistical_analysis import StatisticalAnalysis

def analyze(knowledgeGraph):
  return __top_of_histogram(knowledgeGraph)

def __top_of_histogram(knowledgeGraph):
  topOfHistograms={}
  histograms=__calculate_histograms(knowledgeGraph)
  for token, histoList in histograms.get_report().items():
    topOfHistograms[token]=[]
    topScore=0
    for i in range(0, len(histoList)):
      topLink=None
      for linkedToken, score in histoList[i].items():
        if score > topScore:
          topScore=score
          topLink=linkedToken
      if topLink != None: 
        topOfHistograms[token]=topLink
  return topOfHistograms

def __calculate_histograms(knowledgeGraph):
  histograms=StatisticalAnalysis()
  for tokenAndLinks in knowledgeGraph.get_graph():
    for i in range(0, len(tokenAndLinks[1])):
      histograms.increment_value_of_token_position(tokenAndLinks[0], tokenAndLinks[1][i], i)
  return histograms
