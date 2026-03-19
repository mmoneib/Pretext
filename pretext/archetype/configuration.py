from .constants import *

## Formalization of what is to be configured within the project.
class Configuration:

  def __init__(self, args):
    # Defaults
    ## Reading
    self.commonWordReplacement=None
    ## Tokenization
    self.charsTokenizationSteps = [7,9,13]
    self.wordsTokenizationSteps = [5,7]
    self.numOfTokenizationThreads=1
    self.tokenizationSeparator=""
    ## Modeling
    self.numOfNextTokens=0.7 # Should be used in conjunction with 'predictUptoPosition'. Both may have no effect in case of sliced predictions. 0.1 and more.
    ## Prediction
    #self.fuzzyFallbackSearch=None
    #self.fuzzyFallbackSearch="first match"
    self.infinitePrompting=False
    self.maxNumOfPredictions=1000
    self.maxNumOfWords=1000
    self.predictUptoPosition=0 # Scores each token individually. Might be useful for keywords strict tokens. 0 if numOfNextTokens is <=1.
    self.separateTokensInOutput=True
    self.tokenEvaluationStrategy = arg_tokenEvaluationStrategy_choice_pessimistic
    # Overrides (by command-line parameters)
    if args is not None:
      ## Reading
      if args.common_word_replacement == arg_commonWordReplacement_choice_nothing:
        self.commonWordReplacement=arg_commonWordReplacement_value_nothing
      elif args.common_word_replacement == arg_commonWordReplacement_choice_placeholder:
        self.commonWordReplacement=arg_commonWordReplacement_value_placeholder
      ## Tokenization
      if args.chars_tokenization_steps is not None:
        self.charsTokenizationSteps = args.chars_tokenization_steps
      if args.words_tokenization_steps is not None:
        self.wordsTokenizationSteps = args.words_tokenization_steps
      ## Modeling
      ## Prediction
      self.infinitePrompting=args.infinite_prompting
      self.fuzzyFallbackSearch=args.fuzzy_fallback_search
      self.tokenEvaluationStrategy = args.token_evaluation_strategy
      self.prompt=args.prompt
