class StatisticalAnalysis:
  def __init__(self):
    self.report=[]

  def increment_value_of_token_position(self, token, link, position):
    if self.report[(token, position)] == None or self.report[(token, position)][link] == None:
      linksMap=[]
      linksMap[link]=1
      self.report[(token, position)]=linksMap
    else:
      currValue=self.report[(token, position)][link]
      self.report[(token, position)]=currVal+1

  def get_report(self):
    return report
