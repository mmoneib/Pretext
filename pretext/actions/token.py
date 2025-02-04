# Relative imports are to allow importing from the tests package.
from ..archetype.token_graph import TokenGraph
from ..archetype.token_scores import TokenScores
from ..archetype.token_choices import TokenChoices
import random

# Add separator to avoid mixing between tokens of different granularities when modeling.
def append_tokenization_separator(tokens, separator): #TODO Should this be embedded in tokenization itself? I think so.
  tokens.append(separator)
  return tokens

def model_by_next(numOfNextTokens, tokens, tokenGraph, separator):
  for i in range(0, len(tokens)-1):
     if tokens[i] == separator: # Could have been removed by another action, but better be embeedded as it has no use.
       continue
     # Python gracefully doesn't throw errors when slicing out of bounds.
     if numOfNextTokens >= 1:
       tokenGraph.link(tokens[i], tokens[i+1:i+numOfNextTokens+1])
     elif numOfNextTokens < 1 and numOfNextTokens > 0:
       slicedToken=tokens[i+1][0:round(len(tokens[i+1])*numOfNextTokens)]
       print(tokens[i] +" ||| " +slicedToken)
       tokenGraph.link(tokens[i], [slicedToken])
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

def predict_optimistically(tokenChoices, token, predictUpToPosition, separator):
  step = 1 #TODO Make the steps configurable to make prediction more fuzzy.
  while len(token) > 0:
    choice = None # Must be different from the separator so as to indicate not finding anything (including separator) and only then moving on to slicing the token.
    for p in range(0, predictUpToPosition + 1):
      currentChoice = tokenChoices.get_choice(token, p)
      if currentChoice != None:
        if choice == None:
          choice = ""
        choice += currentChoice
    if choice is not None:
      #print("Token: {}  |  Choice: {}".format(token,choice))
      return choice
    token=token[step:len(token)] # Optimistic flow of evaluation of the prompt from its entirety down to the last character.
  return separator # Explicit finalization in case nothing is found. Highly unlikely in case of fine-grained tokenizzation.

# Instead of adding a new parameter for a common predict method and plague it with ifs, the architectural flow suggest passing the decision of the strategy to the activity and separation the prediction action into 2 for cleaner unit testing.
def predict_pessimistically(tokenChoices, token, predictUpToPosition, separator):
  step = 1 #TODO Make the steps configurable to make prediction more fuzzy.
  initialInclusion = 1 # Number of right-most characters of the token left by the slice.
  fullToken = token
  token = fullToken[len(fullToken)-initialInclusion:len(fullToken)]
  iterativeInclusion = initialInclusion
  while len(fullToken)-iterativeInclusion >= -1: # More fundamental condition than comparing lengths of fullToken and token, which skip the last iteration if no choice is found.
    choice = None # Must be different from the separator so as to indicate not finding anything (including separator) and only then moving on to slicing the token.
    for p in range(0, predictUpToPosition + 1):
      currentChoice = tokenChoices.get_choice(token, p)
      if currentChoice != None:
        if choice == None:
          choice = ""
        choice += currentChoice
    if choice is not None:
      return choice
    token = fullToken[len(fullToken)-iterativeInclusion:len(fullToken)] # Optimistic flow of evaluation of the prompt from its entirety down to the last character.
    iterativeInclusion = iterativeInclusion + step
  return separator # Explicit finalization in case nothing is found. Highly unlikely in case of fine-grained tokenizzation.

def search_in_tokens(tokens, criterion): # A barely smart fuzzy search with the aim of finding relevant tokens.
  found=""
  for t in tokens:
    i = t.find(criterion)
    if i != -1:
      potentialFind=t
      if found=="" or len(potentialFind) < len(found): # As there is no constant for maximum int value in Python 3. Less than because we want the most fitting find.
        found=potentialFind
  return found

def search_startswith_tokens(tokens, criterion): # A non-smart (no statistics involved) fuzzy search wwith the aim of mixing into a flow.
  for t in tokens:
    if t.startswith(criterion) == True: # Returns first find.
#      print("\nsearch_startswith_tokens: Criterion-->{} Token-->{}".format(criterion, t))
      return t.replace(criterion, "", 1) # Replacing the matched starting part for convenience of printing directly after the criterion.
  return ""

def search_startswith_tokens_stochastic(tokens, criterion):
  potentialTokens=[]
  for t in tokens:
    if t.startswith(criterion) == True: # Returns first find.
      potentialTokens.append(t)
  if len(potentialTokens) == 0:
    return ""
  return random.choice(potentialTokens).replace(criterion, "", 1) 

def get_max_size_of_token(tokens):
  maxSize=0
  for t in tokens:
    if len(t) > maxSize:
      maxSize = len(t)
  return maxSize
