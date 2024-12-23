# Relative imports are to allow importing from the tests package.
from ..archetype.token_graph import TokenGraph
from ..archetype.token_scores import TokenScores
from ..archetype.token_choices import TokenChoices

# Add separator to avoid mixing between tokens of different granularities when modeling.
def append_tokenization_separator(tokens, separator): #TODO Should this be embedded in tokenization itself? I think so.
  tokens.append(separator)
  return tokens

def model_by_next(numOfNextTokens, tokens, tokenGraph, separator):
  for i in range(0, len(tokens)-1):
     if tokens[i] == separator: # Could have been removed by another action, but better be embeedded as it has no use.
       continue
     # Python gracefully doesn't throw errors when slicing out of bounds.
     tokenGraph.link(tokens[i], tokens[i+1:i+numOfNextTokens+1])
  return tokenGraph

def top_of_histogram(tokenGraph):
  topOfHistograms=TokenChoices()
  histograms=calculate_histograms(tokenGraph)
  for token, histoList in histograms.get_scores().items():
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
  while len(token) > 0: #TODO Make the steps configurable
    choice=""
    for p in range(0, predictUpToPosition + 1):
      currentChoice = tokenChoices.get_choice(token, p)
      if currentChoice != None:
        choice += currentChoice
    if choice != "":
      return choice
    token=token[1:len(token)] # Optimistic flow of evaluation of the prompt from its entirety down to the last character.
  return "" # We could also return choice, but this is more explicit.
