from actions import text as TextActions
import time

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
    isComplete = True
    return self # For chaining.

  def output_complete(self): # Busy waiting until output is available.
    while isComplete == False:
      time.sleep(1)  
    return self.tokens

  def output_maybe_incomplete(self): # Unguaranteed ouptut in case of multu-threads.
    return self.tokens
