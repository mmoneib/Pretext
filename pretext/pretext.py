#!/usr/bin/python
import argparse
from actions import modeler
from actions import statistician
from actions import tokenizer
from process.reader import ReaderYieldingProcess
from process import writer
from model.configuration import Configuration
from model.knowledge_graph import KnowledgeGraph

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

if __name__=="__main__":
  parser = argparse.ArgumentParser(description="Pretext predicts text based on input document(s) (scope of knowledge), statistical formula (method of analysis), and a trigger text for the output along with its size (destiny).")
  parser.add_argument("-c", "--chars-tokenization-steps", help="list of integers specifying the number of characters considered in each tokenization step", nargs='*')
  parser.add_argument("-k", "--knowledge-files", help="path to files to be added to the scope of knowledge.", nargs='*', required=True)
  parser.add_argument("-n", "--infinite-prompting", help="cycle between prompts and subsequent predictions until |exit| is typed.", action="store_true")
  parser.add_argument("-w", "--words-tokenization-steps", help="list of integers specifying the number of words considered in each tokenization step", nargs='*')
  args = parser.parse_args()
  config=Configuration()
  config.infinitePrompting=args.infinite_prompting
  knowledgeGraph=KnowledgeGraph()
  for output in ReaderYieldingProcess(args.knowledge_files).start():
    tokens=[]
    if args.chars_tokenization_steps:
      for i in args.chars_tokenization_steps:
        tokens.extend(tokenizer.tokenize_by_chars(output, int(i)))
    if args.words_tokenization_steps:
      for i in args.words_tokenization_steps:
        tokens.extend(tokenizer.tokenize_by_words(output, int(i)))
    knowledgeGraph=modeler.model_by_next(tokens, knowledgeGraph)
  print(statistician.top_of_histogram(knowledgeGraph).get_report())
  writer.write(statistician.top_of_histogram(knowledgeGraph),config)
