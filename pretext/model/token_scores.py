## Dict(token : List(Dict(linkedToken:score)))
class TokenScores:
  def __init__(self):
    self.scores={}

  def increment_value_of_token_position(self, token, link, position):
    if self.scores.get(token) == None:
      self.scores[token]=[]
    # IndexError for lists is avoided by len and insert functions.
    if len(self.scores.get(token)) <= position: # len is cheap.
      self.scores[token].insert(position, {})
    if self.scores[token][position].get(link) == None:
      self.scores[token][position][link]=1
    else:
      currValue=self.scores[token][position][link]
      self.scores[token][position][link]=currValue+1

  def get_scores(self):
    print("Scores: ", self.scores)
    return self.scores
