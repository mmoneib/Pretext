#!/usr/bin/python
import argparse
import pretext
from pretext.activity.reading import Reading_YieldingActivity
from pretext.activity.tokenization import Tokenization_ParallelActivity
from pretext.activity.modeling import Modeling_ParallelActivity
from pretext.activity.statistics import Statistics_ProceduralActivity
from pretext.activity.predicting import Predicting_YieldingActivity
from pretext.archetype.configuration import Configuration
from pretext.archetype.token_graph import TokenGraph

def cmd_sync_predefined_prompt():
  parser = argparse.ArgumentParser(description="Pretext predicts text based on input document(s) (scope of knowledge), statistical formula (method of analysis), and a trigger text for the output along with its size (destiny).")
  parser.add_argument("-c", "--chars-tokenization-steps", help="list of integers specifying the number of characters considered in each tokenization step", nargs='*')
  parser.add_argument("-k", "--knowledge-files", help="path to files to be added to the scope of knowledge.", nargs='*', required=True) # nargs produce a list.
  parser.add_argument("-n", "--infinite-prompting", help="cycle between prompts and subsequent predictions until |exit| is typed.", action="store_true")
  parser.add_argument("-w", "--words-tokenization-steps", help="list of integers specifying the number of words considered in each tokenization step", nargs='*')
  parser.add_argument("-e", "--token-evaluation-strategy", help="evaluation of token for prediction can be 'optimistic' trying from full prompt and slicing down, or 'pessimistic' trying from minimally sliced prompt and increasing, or 'mixed' alternating between both.", choices=["optimistic","pessimistc","mixed"])
  args = parser.parse_args()
  config=Configuration(args)
  tokenGraph=TokenGraph()
  for text in Reading_YieldingActivity(config, args.knowledge_files).act():
    tokenizationParallel = Tokenization_ParallelActivity(config, text)
    tokenizationParallel.act()
    tokens=tokenizationParallel.output()
    print("Tokens: ", tokens)
    modelingParallel = Modeling_ParallelActivity(config, tokens, tokenGraph)
    modelingParallel.act()
    tokenGraph = modelingParallel.output()
  print(tokenGraph.get_graph())
  statisticsProcedural = Statistics_ProceduralActivity(tokenGraph)
  statisticsProcedural.act()
  tokenChoices = statisticsProcedural.output()
  print("Report:\n" , tokenChoices.get_choices())
  initialPrompt = "billion"
  initialPrompt = " " + initialPrompt # As tokenization is done with a preceding space.
  predictingYielding = Predicting_YieldingActivity(config, tokenChoices, initialPrompt)
  output = ""
  #print("Prediction:\n")
  for yieldedPrediction in predictingYielding.act():
      print(yieldedPrediction, end='', flush=True)

#TODO Unit test better about the separator.
