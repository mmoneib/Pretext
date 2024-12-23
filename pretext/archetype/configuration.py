## Formalization of what is to be configured within the project.
class Configuration:

  def __init__(self, args):
    # Defaults
    self.charsTokenizationSteps = [1]
    self.infinitePrompting=False
    self.numberOfTokenizationThreads=1
    self.predictUptoPosition=0
    self.tokenizationSeparator="" # Specific to Tokenization as it might not be suitable for other activites.
    self.wordsTokenizationSteps = []
    # Overrides (by command-line parameters)
    if args is not None:
      self.infinitePrompting=args.infinite_prompting
      if args.chars_tokenization_steps is not None:
        self.charsTokenizationSteps = args.chars_tokenization_steps
      if args.words_tokenization_steps is not None:
        self.wordsTokenizationSteps=args.words_tokenization_steps
