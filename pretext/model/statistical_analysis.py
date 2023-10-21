## Dict(token : Dict(position: Dict(linkedToken:score)))
class StatisticalAnalysis:
  def __init__(self):
    self.report={}

  def increment_value_of_token_position(self, token, link, position):
    if self.report.get(token) == None:
      self.report[token]={} # Not a list despite having positions as key because insertion may not be in order. Alse easier access.
    if self.report.get(token).get(position) == None:
      self.report[token][position]={}
    if self.report[token][position].get(link) == None:
      self.report[token][position][link]=1
    else:
      currValue=self.report[token][position][link]
      self.report[token][position][link]=currValue+1

  def get_report(self):
    print(self.report)
    return self.report
