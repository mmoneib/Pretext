from model.token_graph import TokenGraph
from model.token_score import TokenScore
from model.token_choice import TokenChoice

def model_by_next(tokens, tokenGraph):
  for i in range(0, len(tokens)-1):
    tokenGraph.link(tokens[i], [tokens[i+1]])
    tokenGraph.link(tokens[i+1], [""])
  return tokenGraph

def top_of_histogram(tokenGraph):
  topOfHistograms=TokenChoice()
  histograms=calculate_histograms(tokenGraph)
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

def calculate_histograms(tokenGraph):
  histograms=TokenScore()
  for tokenAndLinks in tokenGraph.get_graph():
    for i in range(0, len(tokenAndLinks[1])):
      histograms.increment_value_of_token_position(tokenAndLinks[0], tokenAndLinks[1][i], i)
  return histograms
