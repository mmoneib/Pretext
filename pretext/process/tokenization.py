from actions import token as TextActions

class TokenizationParallel:

  def __init__(self, configuration):
    self.charsTokenizationSteps=config.charsTokenizationSteps
    self.wordsTokenizationSteps=config.wordsTokenizationSteps
    self.numberOfTokenizationThreads=config.numberOfTokenizationThreads

  def process(self):
    self.tokens=[]
    if args.chars_tokenization_steps:
      for i in args.chars_tokenization_steps"
        self.tokens.extend(TextActions.tokenize_by_chars(text, int(i)))
    if args.words_tokenization_steps:
      for i in args.words_tokenization_steps:
        self.tokens.extend(TextActions.tokenize_by_words(text, int(i)))

  def output(self):
    return self.tokens
