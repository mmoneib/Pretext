#!/usr/bin/python
import argparse
from actions import text as TextActions
from actions import token as TokenActions
from process.reading import ReadingYieldingProcess
from process.tokenization import TokenizationParallel
from process import writing
from model.configuration import Configuration
from model.token_graph import TokenGraph

#TODO Check feasibility of tokenization by keywords.
#TODO Persist the models.
#TODO Make process modules into classes of input, process, and output workflow.
#TODO Add logging.
#TODO Add header comments to functions.
#TODO Add more unit tests for effect of empty spaces on tokenization.
#TODO ALlow assymmetrical modeling, like 3 unconsecutive chars predicting a word (instead of another 2 unconsecutive chars).
#TODO Parse input directories.
#TODO Use tokenization steps as an input parameter.
#TODO validate tokenization by 2 chars.
#TODO Add process for each actions type to allow for distributive execution.
#TODO Add multithreading to TokenizationParallel. Also, add blocking/non-blocking retrieval.

if __name__=="__main__":
  parser = argparse.ArgumentParser(description="Pretext predicts text based on input document(s) (scope of knowledge), statistical formula (method of analysis), and a trigger text for the output along with its size (destiny).")
  parser.add_argument("-c", "--chars-tokenization-steps", help="list of integers specifying the number of characters considered in each tokenization step", nargs='*')
  parser.add_argument("-k", "--knowledge-files", help="path to files to be added to the scope of knowledge.", nargs='*', required=True)
  parser.add_argument("-n", "--infinite-prompting", help="cycle between prompts and subsequent predictions until |exit| is typed.", action="store_true")
  parser.add_argument("-w", "--words-tokenization-steps", help="list of integers specifying the number of words considered in each tokenization step", nargs='*')
  args = parser.parse_args()
  config=Configuration()
  config.infinitePrompting=args.infinite_prompting
  config.charsTokenizationSteps=args.chars_tokenization_steps
  tokenGraph=TokenGraph()
  for text in ReaderYieldingProcess(args.knowledge_files).process():
    tokenizationParallel = TokenizationParallel(config)
    tokenizationParallel.process()
    tokens=tokenizationParallel.output()
    tokenGraph=TokenActions.model_by_next(tokens, tokenGraph)
  print(TokenActions.top_of_histogram(tokenGraph).get_report())
  writing.write(TokenActions.top_of_histogram(tokenGraph),config)
