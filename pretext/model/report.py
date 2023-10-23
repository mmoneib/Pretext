## Dict(token : Dict(position: chosenLinkedToken))
class Report:
  def __init__(self):
    self.report={}

  def add_choice(self, token, position, chosenLinkedToken):
    if self.report.get(token) == None:
      self.report[token]={}
    self.report[token][position]=chosenLinkedToken

  def get_choice (self, token, position):
    positionalReportedTokens=self.report.get(token)
    if positionalReportedTokens != None:
      return  self.report.get(token).get(position)
    else:
      return None

  def get_report(self):
    return self.report
    
