#!/usr/bin/python
import argparse
import pretext
from pretext.activity.reading import Reading_YieldingActivity
from pretext.activity.tokenization import Tokenization_ParallelActivity
from pretext.activity.modeling import Modeling_ParallelActivity
from pretext.activity.statistics import Statistics_ProceduralActivity
from pretext.activity.predicting import Predicting_YieldingActivity
from pretext.archetype.configuration import Configuration
from pretext.archetype.constants import *
from pretext.archetype.token_graph import TokenGraph

def cmd_sync_predefined_prompt():
  print ("Initializing through command line...")
  parser = argparse.ArgumentParser(description="Pretext predicts text based on input document(s) (scope of knowledge), statistical formula (method of analysis), and a trigger text for the output along with its size (destiny).")
  parser.add_argument("-c", "--chars-tokenization-steps", help="list of integers specifying the number of characters considered in each tokenization step", nargs='*', type=int)
  parser.add_argument("-e", "--token-evaluation-strategy", help="evaluation of token for prediction can be 'optimistic' trying from full prompt and slicing down, or 'pessimistic' trying from minimally sliced prompt and increasing, or 'mixed' alternating between both.", choices=[arg_tokenEvaluationStrategy_choice_optimistic,arg_tokenEvaluationStrategy_choice_pessimistic,arg_tokenEvaluationStrategy_choice_mixed])
  parser.add_argument("-f", "--fuzzy-fallback-search", help="search using partial tokens in case no full one is found.", choices=[arg_fuzzyFallbackSearch_choice_firstMatch, arg_fuzzyFallbackSearch_choice_stochastic])
  parser.add_argument("-k", "--knowledge-files", help="path to files to be added to the scope of knowledge.", nargs='*', required=True) # nargs produce a list.
  parser.add_argument("-n", "--infinite-prompting", help="cycle between prompts and subsequent predictions until |exit| is typed.", action="store_true")
  parser.add_argument("-p", "--prompt", help="prompt acting as the initial part of the text to be predicted.")
  parser.add_argument("-r", "--common-word-replacement", help="replace articles, conjunctions, and propositions from texts prior to tokenization.", choices=[arg_commonWordReplacement_choice_nothing, arg_commonWordReplacement_choice_placeholder])
  parser.add_argument("-w", "--words-tokenization-steps", help="list of integers specifying the number of words considered in each tokenization step", nargs='*', type=int)
  print ("Parsing input arguments...")
  args = parser.parse_args()
  print ("Setting up configuration...")
  config=Configuration(args)
  tokenGraph=TokenGraph()
  print ("Starting tokenization and modeling activites...")
  for text in Reading_YieldingActivity(config, args.knowledge_files).act():
    tokenizationParallel = Tokenization_ParallelActivity(config, text)
    tokenizationParallel.act()
    tokens=tokenizationParallel.output()
    print("Tokens: ", tokens)
    modelingParallel = Modeling_ParallelActivity(config, tokens, tokenGraph)
    modelingParallel.act()
    tokenGraph = modelingParallel.output()
  print(tokenGraph.get_graph())
  print ("Starting modeling activity...")
  statisticsProcedural = Statistics_ProceduralActivity(tokenGraph)
  statisticsProcedural.act()
  tokenChoices = statisticsProcedural.output()
  print("Report:\n" , tokenChoices.get_choices())
  if config.prompt is None:
      print("Prediction skipped as no prompt was provided.")
      exit()
  initialPrompt = config.prompt
  print("Starting predicting activity...")
  predictingYielding = Predicting_YieldingActivity(config, tokenChoices, initialPrompt)
  output = ""
  for yieldedPrediction in predictingYielding.act():
      print(yieldedPrediction, end='', flush=True)

