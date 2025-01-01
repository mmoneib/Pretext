## Formalization of what is to be configured within the project.
class Configuration:

  def __init__(self, args):
    # Defaults
    self.charsTokenizationSteps = [] # Important for partial matching of prompts but causes infinite loops and non-sensical output.
    self.infinitePrompting=False
    self.numOfNextTokens=3 # More than 1, gives opportunity for larger tokens to hit, favors copying as-is.
    self.numberOfTokenizationThreads=1
    self.predictUptoPosition=3 # Scores each token individually. Might be useful for keywords strict tokens.
    self.commonWordReplacement=""
    self.tokenizationSeparator="" # Specific to Tokenization as it might not be suitable for other activites.
    self.wordsTokenizationSteps = [3,5,7,9,11]
    # Overrides (by command-line parameters)
    if args is not None:
      self.infinitePrompting=args.infinite_prompting
      if args.chars_tokenization_steps is not None:
        self.charsTokenizationSteps = args.chars_tokenization_steps
      if args.words_tokenization_steps is not None:
        self.wordsTokenizationSteps=args.words_tokenization_steps
