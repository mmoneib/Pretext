def write(report, futurePositions):
  __write_with_prompt(report, futurePositions)

def __write_with_prompt(report, futurePositions):
  prompt=input("Enter prompt: ")
  print("Suggestion: " + __evaluatePrediction(report, futurePositions, prompt))

def __evaluatePrediction(report, futurePosition, prompt):
  choice=None
  while len(prompt) > 0: #TODO Make the steps configurable
    choice=report.get_choice(prompt, futurePosition)
    prompt=prompt[1:len(prompt)]
  return choice
