#!/usr/bin/python
import argparse
import pretext
from pretext.activity.reading import Reading_YieldingActivity
from pretext.activity.tokenization import Tokenization_ParallelActivity
from pretext.activity.modeling import Modeling_ParallelActivity
from pretext.activity.statistics import Statistics_ProceduralActivity
from pretext.activity.writing import WritingProcedural
from pretext.archetype.configuration import Configuration
from pretext.archetype.token_graph import TokenGraph

#TODO Check feasibility of tokenization by keywords.
#TODO Persist the.archetype..
#TODO Make activity modules into classes of input, activity, and output workflow.
#TODO Add logging.
#TODO Add header comments to functions.
#TODO Parse input directories.
#TODO Use tokenization steps as an input parameter.
#TODO Add multithreading to Tokenization_ParallelActivity and Modeling_ParallelActivity.
#TODO Should we tokenize starting from every unit of text? or just from the end of the last token?
#TODO What would bring the generation to a closure?
#TODO Make all config parameters available in the command line.
#TODO Add integration tests.
#TODO Ability to mix threading with multiprocesses.

if __name__=="__main__":
  parser = argparse.ArgumentParser(description="Pretext predicts text based on input document(s) (scope of knowledge), statistical formula (method of analysis), and a trigger text for the output along with its size (destiny).")
  parser.add_argument("-c", "--chars-tokenization-steps", help="list of integers specifying the number of characters considered in each tokenization step", nargs='*')
  parser.add_argument("-k", "--knowledge-files", help="path to files to be added to the scope of knowledge.", nargs='*', required=True) # nargs produce a list.
  parser.add_argument("-n", "--infinite-prompting", help="cycle between prompts and subsequent predictions until |exit| is typed.", action="store_true")
  parser.add_argument("-w", "--words-tokenization-steps", help="list of integers specifying the number of words considered in each tokenization step", nargs='*')
  args = parser.parse_args()
  config=Configuration(args)
  tokenGraph=TokenGraph()
  for text in Reading_YieldingActivity(args.knowledge_files).act():
    tokenizationParallel = Tokenization_ParallelActivity(config, text)
    tokenizationParallel.act()
    tokens=tokenizationParallel.output()
    print("Tokens: ", tokens)
    modelingParallel = Modeling_ParallelActivity(tokens, tokenGraph)
    modelingParallel.act()
    tokenGraph = modelingParallel.output()
  print(tokenGraph.get_graph())
  statisticsProcedural = Statistics_ProceduralActivity(tokenGraph)
  statisticsProcedural.act()
  tokenChoices = statisticsProcedural.output()
  print("Report:\n" , tokenChoices.get_choices())
  writingProcedural = WritingProcedural(tokenChoices, config)
  writingProcedural.act()
