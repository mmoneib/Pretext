from actions import token as TokenActions

class WritingProcedural:

  def __init__(self, tokenChoices, config):
    self.tokenChoices = tokenChoices
    self.predictUptoPosition = config.predictUptoPosition
    self.infinitePrompting = config.infinitePrompting

  def process(self):
    self.__write_with_prompt()
    return self

  def __write_with_prompt(self):
    print("Welcome to Pretext's chat. Write a prompt to get a predicted text or |exit| to exit the chat.")
    while True:
      prompt=input("Enter prompt: ")
      if prompt == "|exit|":
        print("Prompted to exit the chat. Bye!")
        break
      prediction=TokenActions.predict(self.tokenChoices, prompt, self.predictUptoPosition)
      if prediction == None:
        prediction=""
      print("Suggestion: " + prediction )
      if self.infinitePrompting == False:
        break

  def output(self):
    print("")
