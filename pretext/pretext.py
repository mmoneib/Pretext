#!/usr/bin/python
import argparse
from actions import tokenizer
from actions import modeler
from process import reader
from process import statistician
from process import writer
from model.configuration import Configuration
from model.knowledge_graph import KnowledgeGraph

#TODO Allow differing grains of tokenization: 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144 chars, words, and keywords.
#TODO Persist the models.
#TODO Make process modules int classes of input, process, and output workflow.
#TODO Add logging.
#TODO Add header comments to functions.
#TODO Distinguish between word and part of word, like to and token.

if __name__=="__main__":
  parser = argparse.ArgumentParser(description='Pretext predicts text based on input document(s) (scope of knowledge), statistical formula (method of analysis), and a trigger text for the output along with its size (destiny).')
  parser.add_argument('--knowledge-files', nargs='*',
                    help='path to a file to be added to the cope of knowledge.')
  args = parser.parse_args()
  config=Configuration()
  config.infinitePrompting=True
  knowledgeGraph=KnowledgeGraph()
  for output in reader.read(args.knowledge_files):
    tokens=tokenizer.tokenize_by_char(output)
    tokens.extend(tokenizer.tokenize_by_word(output)) # Merges the results of tokenizer with the previous results.
    knowledgeGraph=modeler.model_by_next(tokens, knowledgeGraph)
  print()
  print(statistician.analyze(knowledgeGraph).get_report())
  writer.write(statistician.analyze(knowledgeGraph),config)
