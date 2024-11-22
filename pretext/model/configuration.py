class Configuration:
  def __init__(self, args):
    self.predictUptoPosition=0
    self.infinitePrompting=False
    self.infinitePrompting=args.infinite_prompting
    self.charsTokenizationSteps=args.chars_tokenization_steps
    if self.charsTokenizationSteps is None:
      self.charsTokenizationSteps = 1
    self.wordsTokenizationSteps=args.words_tokenization_steps
    if self.wordsTokenizationSteps is None:
      self.wordsTokenizationSteps = 1
    self.numberOfTokenizationThreads=1
