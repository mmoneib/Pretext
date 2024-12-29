#!/usr/bin/python
import pretext.assemblage.command_line as command_line

#TODO Check feasibility of tokenization by keywords.
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

if __name__=="__main__":
  command_line.cmd_sync_predefined_prompt()
