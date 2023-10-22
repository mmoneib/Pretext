from model.analysis import Analysis
from model.report import Report

def analyze(knowledgeGraph):
  return __top_of_histogram(knowledgeGraph)

def __top_of_histogram(knowledgeGraph):
  topOfHistograms=Report()
  histograms=__calculate_histograms(knowledgeGraph)
  for token, histoList in histograms.get_analysis().items():
    topScore=0
    for i in range(0, len(histoList)):
      topLink=None
      for linkedToken, score in histoList[i].items():
        if score > topScore:
          topScore=score
          topLink=linkedToken
      if topLink != None: 
        topOfHistograms.add_choice(token,i,topLink)
  return topOfHistograms

def __calculate_histograms(knowledgeGraph):
  histograms=Analysis()
  for tokenAndLinks in knowledgeGraph.get_graph():
    for i in range(0, len(tokenAndLinks[1])):
      histograms.increment_value_of_token_position(tokenAndLinks[0], tokenAndLinks[1][i], i)
  return histograms
