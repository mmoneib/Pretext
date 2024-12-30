from ..actions import token as TokenActions

class Writing_InteractiveActivity:

  def __init__(self, config, tokenChoices):
    self.tokenChoices = tokenChoices
    self.predictUptoPosition = config.predictUptoPosition
    self.tokenizationSeparator = config.tokenizationSeparator
    self.infinitePrompting = config.infinitePrompting
    self.infiniteFeedback = False # TODO Add to config.

  def act(self):
    self.__write_with_prompt()
    return self

  def __write_with_prompt(self):
    print("Welcome to Pretext's chat. Write a prompt to get a predicted text or |exit| to exit the chat.")
    interactivity = True
    while True:
      prompt=input("Enter prompt: ")
      if prompt == "|exit|":
        print("Prompted to exit the chat. Bye!")
        break
      prediction=TokenActions.predict(self.tokenChoices, prompt, self.predictUptoPosition)
      #if prediction == None:
      #  prediction=""
      print("Suggestion: " + prediction )
      if self.infinitePrompting == False:
        break

class Predicting_YieldingActivity:
  
  def __init__(self, config, tokenChoices, initialPrompt):
    self.tokenChoices = tokenChoices
    self.predictUptoPosition = config.predictUptoPosition
    self.tokenizationSeparator = config.tokenizationSeparator
    self.initialPrompt = initialPrompt

  def act(self):
    prediction = TokenActions.predict(self.tokenChoices, self.initialPrompt, self.predictUptoPosition, self.tokenizationSeparator)
    prompt = self.initialPrompt + prediction
    count=1 # As already one prediction is done.
    maxNumOfPredictions = 1000
    while prediction != self.tokenizationSeparator:
      count = count + 1
      if (count >= maxNumOfPredictions): # Mat indicates a certain circular referencing infinite loop:
        print("....and so on.\n\nP.S. The graph of tokens may have circular references. To improve the results, tweak the granularity more towards coarse-grained tokens.")
        break
      yield prediction
      prediction = TokenActions.predict(self.tokenChoices, prompt, self.predictUptoPosition, self.tokenizationSeparator)
      prompt = prompt + prediction
    #print("Tokenization separator found. Prediction: " + prediction)

