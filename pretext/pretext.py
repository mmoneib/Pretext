#!/usr/bin/python
import argparse
from actions import text as TextActions
from actions import token as TokenActions
from process.reading import ReadingYieldingProcess
from process.tokenization import TokenizationParallel
from process.modeling import ModelingParallel
from process.statistics import StatisticsProcedural
from process.writing import WritingProcedural
from model.configuration import Configuration
from model.token_graph import TokenGraph

#TODO Check feasibility of tokenization by keywords.
#TODO Persist the models.
#TODO Make process modules into classes of input, process, and output workflow.
#TODO Add logging.
#TODO Add header comments to functions.
#TODO Add more unit tests for effect of empty spaces on tokenization.
#TODO Allow assymmetrical modeling, like 3 unconsecutive chars predicting a word (instead of another 2 unconsecutive chars).
#TODO Parse input directories.
#TODO Use tokenization steps as an input parameter.
#TODO validate tokenization by 2 chars.
#TODO Add process for each actions type to allow for distributive execution.
#TODO Add multithreading to TokenizationParallel and ModelingParallel.
#TODO Should we tokenize starting from every unit of text? or just from the end of the last token?

if __name__=="__main__":
  parser = argparse.ArgumentParser(description="Pretext predicts text based on input document(s) (scope of knowledge), statistical formula (method of analysis), and a trigger text for the output along with its size (destiny).")
  parser.add_argument("-c", "--chars-tokenization-steps", help="list of integers specifying the number of characters considered in each tokenization step", nargs='*')
  parser.add_argument("-k", "--knowledge-files", help="path to files to be added to the scope of knowledge.", nargs='*', required=True)
  parser.add_argument("-n", "--infinite-prompting", help="cycle between prompts and subsequent predictions until |exit| is typed.", action="store_true")
  parser.add_argument("-w", "--words-tokenization-steps", help="list of integers specifying the number of words considered in each tokenization step", nargs='*')
  args = parser.parse_args()
  config=Configuration(args)
  tokenGraph=TokenGraph()
  for text in ReadingYieldingProcess(args.knowledge_files).process():
    tokenizationParallel = TokenizationParallel(config, text)
    tokenizationParallel.process()
    tokens=tokenizationParallel.output()
    print("Tokens: ", tokens)
    modelingParallel = ModelingParallel(tokens, tokenGraph)
    modelingParallel.process()
    tokenGraph = modelingParallel.output()
  print(tokenGraph.get_graph())
  statisticsProcedural = StatisticsProcedural(tokenGraph)
  statisticsProcedural.process()
  tokenChoices = statisticsProcedural.output()
  print("Report:\n" , tokenChoices.get_report())
  writingProcedural = WritingProcedural(tokenChoices, config)
  writingProcedural.process()
