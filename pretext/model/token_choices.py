## Dict(token : Dict(position: chosenLinkedToken))
class TokenChoices:
  def __init__(self):
    self.report={}

  def add_choice(self, token, position, chosenLinkedToken):
    if self.report.get(token) == None:
      self.report[token]={}
    #print("Added Token:", token, " ", position, " ", chosenLinkedToken)
    self.report[token][position]=chosenLinkedToken

  def get_choice(self, token, position):
    positionalReportedTokens=self.report.get(token)
    if positionalReportedTokens != None:
      #print(self.report.get(token).get(position))
      return self.report.get(token).get(position)
    else:
      return None

  def get_report(self):
    print("Report: ", self.report)
    return self.report
    
