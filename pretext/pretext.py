#!/usr/bin/python
import argparse
import reader
import tokenizer
import modeler
import statistician
from knowledge_graph import KnowledgeGraph

if __name__=="__main__":
  parser = argparse.ArgumentParser(description='Pretext predicts text based on input document(s) (scope of knowledge), statistical formula (method of analysis), and a trigger text for the output along with its size (destiny).')
  parser.add_argument('--knowledge-files', nargs='*',
                    help='path to a file to be added to the cope of knowledge.')
  args = parser.parse_args()
  knowledgeGraph=KnowledgeGraph()
  for output in reader.read(args.knowledge_files):
    knowledgeGraph=modeler.model(tokenizer.tokenize(output), knowledgeGraph)
  statistician.analyze(knowledgeGraph)
