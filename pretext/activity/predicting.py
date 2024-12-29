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
    #print("Initial prompt: " + self.initialPrompt)
    #print("Prediciton: " + prediction)
    #print("Prompt: " + prompt)
    count=0
    while prediction != self.tokenizationSeparator:
      yield prediction
      prediction = TokenActions.predict(self.tokenChoices, prompt, self.predictUptoPosition, self.tokenizationSeparator)
      prompt = prompt + prediction
      #print("Prediciton: " + prediction)
      #print("Prompt: " + prompt)
     # count=count+1
      #if count ==5:
       # exit()
    print("Tokenization separator found. Prediction: " + prediction)
