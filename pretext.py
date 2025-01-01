#!/usr/bin/python
import pretext.assemblage.command_line as command_line

#TODO Remove outlier tokens with highest frequencies from the model.
#TODO Persist the archetype.
#TODO Add logging.
#TODO Add header comments to functions.
#TODO Parse input directories.
#TODO Add multithreading to Tokenization_ParallelActivity and Modeling_ParallelActivity.
#TODO Should we tokenize starting from every unit of text? or just from the end of the last token?
#TODO Make all config parameters available in the command line.
#TODO Add functional tests.
#TODO Ability to mix threading with multiprocesses.
#TODO Separate tokenization into more granular activities, so that it doesn't have to be one activity per text (file).
#TODO Remove redundancy of 'output' functions from activities. Use inheritemce?
#TODO Fix or prevent infinite loop at fine-grained (character) predictions when a token predict itself or 2 predict each others. Timeout?
#TODO Add statistics based on random choice.
#TODO Add separaotr for certain finalizaiton which would be based on the desired output.
#TODO Add optimization by disallowing slicing the prompt with a size more than that of the largest token. Could be applicable only to some statistics like histogram.
#TODO Add limitation of output by number of characters and words.
#TODO Add ignore_case option for tokenization and retrieval.
#TODO Values in choices of sizes different from token. Otherwise, a value of the same size will always be found.
#TODO Fuzzy matching of tokens.
#TODO Remove implicit default configs and make them required.
#TODO Make common words configurable.
#TODO Add report about the number of references per token?
#TODO Slice from smallest right part of prompt, increasing leftward.
#TODO Alternate between both sides of slicing.
# For TopOfHistogram statistics, there are 2 traps: Tokenization by small number of chars increase probability of infinite loops of circular references. Tokenization by large number of words increase the probability of output flowing only from a single input document. Alsom when choices are of the same size as tokens, a solution will also be found at that size, which increases the probability of those traps. The circular reference trap is mainly due to redundancy in languages.

if __name__=="__main__":
  command_line.cmd_sync_predefined_prompt()
