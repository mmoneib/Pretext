## Formalization of what is to be configured within the project.
class Configuration:

  def __init__(self, args):
    # Defaults
    self.charsTokenizationSteps = []
    self.commonWordReplacement=""
    self.infinitePrompting=False
    self.maxNumOfPredictions=1000
    self.maxNumOfWords=1000
    self.numOfNextTokens=1 # Should be used in conjunction with 'predictUptoPosition'. Both may have no effect in case of sliced predictions. 0.1 and more.
    self.numOfTokenizationThreads=1
    self.predictUptoPosition=0 # Scores each token individually. Might be useful for keywords strict tokens. 0 if numOfNextTokens is <=1.
    self.tokenEvaluationStrategy = "optimistic"
    #self.tokenEvaluationStrategy = "pessimistic"
    #self.tokenEvaluationStrategy = "mixed"
    self.tokenizationSeparator=""
    self.wordsTokenizationSteps = [8,10,12]
    # Overrides (by command-line parameters)
    if args is not None:
      self.infinitePrompting=args.infinite_prompting
      if args.chars_tokenization_steps is not None:
        self.charsTokenizationSteps = args.chars_tokenization_steps
      if args.words_tokenization_steps is not None:
        self.wordsTokenizationSteps=args.words_tokenization_steps
