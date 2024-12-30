## Dict(token : List(chosenLinkedToken)
class TokenChoices:
  def __init__(self):
    self.choices={}

  def add_choice(self, token, position, chosenLinkedToken):
    if self.choices.get(token) == None:
      self.choices[token]=[]
    #print("Added Token:", token, " ", position, " ", chosenLinkedToken)
    self.choices[token].insert(position, chosenLinkedToken)

  def get_choice(self, token, position):
    positionalReportedTokens=self.choices.get(token)
    if positionalReportedTokens != None and len(positionalReportedTokens) > position:
      return positionalReportedTokens[position]
    else:
      return None

  def get_choices(self):
    print("Choices: ", self.choices)
    return self.choices

  def get_number_of_tokens(self):
    return len(self.choices.keys())

