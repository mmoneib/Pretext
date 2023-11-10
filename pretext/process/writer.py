def write(report, config):
  __write_with_prompt(report, config)

def __write_with_prompt(report, config):
  print("Welcome to Pretext's chat. Write a prompt to get a predicted text or |exit| to exit the chat.")
  while True:
    prompt=input("Enter prompt: ")
    if prompt == "|exit|":
      print("Prompted to exit the chat. Bye!")
      break
    prediction=__predict(report, prompt, config)
    if prediction == None:
      prediction=""
    print("Suggestion: " + prediction )
    if config.infinitePrompting == False:
      break

def __predict(report, prompt, config):
  choice=None
  while len(prompt) > 0: #TODO Make the steps configurable
    choice=report.get_choice(prompt, config.predictUptoPosition)
    if choice != None:
      return choice
    prompt=prompt[1:len(prompt)] # Optimistic evaluation of the prompt from its entirety down to the last character.
  return ""
