#!/usr/bin/python
import argparse
from process import reader
from process import tokenizer
from process import modeler
from process import statistician
from process import writer
from model.knowledge_graph import KnowledgeGraph

#TODO Allow differing grains of tokenization: 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144 chars, words, and keywords.
#TODO Persist the models.
#TODO Create input and prediction.

if __name__=="__main__":
  parser = argparse.ArgumentParser(description='Pretext predicts text based on input document(s) (scope of knowledge), statistical formula (method of analysis), and a trigger text for the output along with its size (destiny).')
  parser.add_argument('--knowledge-files', nargs='*',
                    help='path to a file to be added to the cope of knowledge.')
  args = parser.parse_args()
  knowledgeGraph=KnowledgeGraph()
  for output in reader.read(args.knowledge_files):
    knowledgeGraph=modeler.model(tokenizer.tokenize(output), knowledgeGraph)
    #print()
    #print(knowledgeGraph.get_graph())
  print()
  print(statistician.analyze(knowledgeGraph).get_report())
  writer.write(statistician.analyze(knowledgeGraph),0)
