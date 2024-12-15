## Formalization of what is to be configured within the project.
class Configuration:

  def __init__(self, args):
    # Defaults
    self.charsTokenizationSteps = 1
    self.infinitePrompting=False
    self.numberOfTokenizationThreads=1
    self.predictUptoPosition=0
    self.wordsTokenizationSteps = 1
    # Overrides
    if args is not None:
      self.infinitePrompting=args.infinite_prompting
      if self.charsTokenizationSteps is not None:
        self.charsTokenizationSteps=args.chars_tokenization_steps
      if self.wordsTokenizationSteps is not None:
        self.wordsTokenizationSteps=args.words_tokenization_steps
