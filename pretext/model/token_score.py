## Dict(token : Dict(position: Dict(linkedToken:score)))
class TokenScore:
  def __init__(self):
    self.analysis={}

  def increment_value_of_token_position(self, token, link, position):
    if self.analysis.get(token) == None:
      self.analysis[token]={} # Not a list despite having positions as key because insertion may not be in order. Alse easier access.
    if self.analysis.get(token).get(position) == None:
      self.analysis[token][position]={}
    if self.analysis[token][position].get(link) == None:
      self.analysis[token][position][link]=1
    else:
      currValue=self.analysis[token][position][link]
      self.analysis[token][position][link]=currValue+1

  def get_analysis(self):
    #print(self.analysis)
    return self.analysis
