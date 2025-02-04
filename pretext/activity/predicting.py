from ..actions import token as TokenActions
from ..actions import text as TextActions

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
    self.charsTokenizationSteps = config.charsTokenizationSteps
    self.fuzzyFallbackSearch = config.fuzzyFallbackSearch
    self.maxNumOfPredictions = config.maxNumOfPredictions
    self.maxNumOfWords = config.maxNumOfWords
    self.predictUptoPosition = config.predictUptoPosition
    self.separateTokensInOutput = config.separateTokensInOutput
    self.tokenizationSeparator = config.tokenizationSeparator
    self.tokenEvaluationStrategy = config.tokenEvaluationStrategy
    self.tokenChoices = tokenChoices
    self.initialPrompt = initialPrompt

  def act(self):
    funcs = (TokenActions.predict_optimistically,TokenActions.predict_pessimistically)
    if self.tokenEvaluationStrategy == "optimistic" or self.tokenEvaluationStrategy == "mixed":
      func = funcs[0]
    elif self.tokenEvaluationStrategy == "pessimistic":
      func = funcs[1]
    prediction = func(self.tokenChoices, self.initialPrompt, self.predictUptoPosition, self.tokenizationSeparator)
    if prediction == "":
      token = TokenActions.search_in_tokens(self.tokenChoices.get_tokens(), self.initialPrompt) # Fuzziness through inclustion.
      prediction = func(self.tokenChoices, token, self.predictUptoPosition, self.tokenizationSeparator)
    prompt = prediction
    countPredictions=1 # As already one prediction is done.
    countWords = 0
    maxTokenSize=TokenActions.get_max_size_of_token(self.tokenChoices.get_tokens())
    predictedSet=set() # To detect and stop repititions in case of non stochastic flows.
    while prediction != self.tokenizationSeparator:
      if prediction in predictedSet: # This test won't be valid for stochastic or inherently cyclic flows.
        print("...but I don't want to repeat myself.")
        break
      else:
        predictedSet.add(prediction)
      if self.tokenEvaluationStrategy == "mixed":
        func = funcs[countPredictions%2] # Alternate between methods.
      countPredictions = countPredictions + 1
      countWords = countWords + TextActions.count_words(prediction)
      if (countPredictions >= self.maxNumOfPredictions): # May indicates a certain circular referencing infinite loop:
        print("....and so on.\n\nP.S. The graph of tokens may have circular references. To improve the results, tweak the granularity more towards coarse-grained tokens.")
        break
      if (countWords > self.maxNumOfWords):
        print("....and so on.\n\nP.S. Maximum number of words achieved.")
        break
      if self.separateTokensInOutput == True:
        prediction = prediction + "|"
      yield prediction
      prediction = func(self.tokenChoices, prompt, self.predictUptoPosition, self.tokenizationSeparator)
      if prediction == "" and self.fuzzyFallbackSearch != None:
        if self.fuzzyFallbackSearch == "first match":
          fallbackFunc = TokenActions.search_startswith_tokens
        elif self.fuzzyFallbackSearch == "stochastic":
          fallbackFunc = TokenActions.search_startswith_tokens_stochastic
        begin = len(prompt) - maxTokenSize  # Try to match with larger criterion.
        while prediction == "" and begin < len(prompt):
          prediction = fallbackFunc(self.tokenChoices.get_tokens(), prompt[begin:]) # Fuzziness by partial search; no predicition.
          begin = begin + 1
      prompt = prompt + prediction
    #print("Tokenization separator found. Prediction: " + prediction)

