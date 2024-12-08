# Relative imports are to allow importing from the tests package.
from ..model.token_graph import TokenGraph
from ..model.token_scores import TokenScores
from ..model.token_choices import TokenChoices

def model_by_next(numOfNextTokens, tokens, tokenGraph):
  for i in range(0, len(tokens)-1):
     # Python gracefully doesn't throw errors when slicing out of bounds.
     tokenGraph.link(tokens[i], tokens[i+1:i+numOfNextTokens+1])
  return tokenGraph

def top_of_histogram(tokenGraph):
  topOfHistograms=TokenChoices()
  histograms=calculate_histograms(tokenGraph)
  for token, histoList in histograms.get_analysis().items():
    print(token, "|" ,histoList)
    for i in range(0, len(histoList)):
      topScore=0
      topLink=None
      for linkedToken, score in histoList[i].items():
        if score > topScore:
          topScore=score
          topLink=linkedToken
      if topLink != None:
        topOfHistograms.add_choice(token,i,topLink)
  return topOfHistograms

def calculate_histograms(tokenGraph):
  histograms=TokenScores()
  for tokenAndLinks in tokenGraph.get_graph():
    for i in range(0, len(tokenAndLinks[1])):
      histograms.increment_value_of_token_position(tokenAndLinks[0], tokenAndLinks[1][i], i)
  return histograms

def predict(tokenChoices, token, predictUpToPosition):
  choice=None
  while len(token) > 0: #TODO Make the steps configurable
    choice=tokenChoices.get_choice(token, predictUpToPosition)
    if choice != None:
      return choice
    token=token[1:len(token)] # Optimistic evaluation of the prompt from its entirety down to the last character.
  return ""
