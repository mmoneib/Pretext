#!/usr/bin/python
import unittest
from pretext.activity.predicting import Predicting_YieldingActivity
from pretext.archetype.configuration import Configuration
from pretext.archetype.token_choices import TokenChoices

class TestPredictingActivity(unittest.TestCase):

  def test_predicting_yealding_finalized_flat_0_upto_position_0(self):
    config = Configuration(None) # None will use defaults.
    config.predictUptoPosition = 0
    config.tokenizationSeparator = ""
    tokenChoices = TokenChoices()
    tokenChoices.add_choice("a", 0, "b")
    tokenChoices.add_choice("b", 0, "c")
    tokenChoices.add_choice("c", 0, "de")
    tokenChoices.add_choice("de", 0, "") # Finalization by separator.
    tokenChoices.add_choice("e", 0, "x")
    initialPrompt = "a"
    activity = Predicting_YieldingActivity(config, tokenChoices, initialPrompt)
    output = ""
    for s in activity.act():
      output += s
    self.assertEqual(output, "bcde")
    tokenChoices.add_choice("b", 0, "x") # Replacement.
    tokenChoices.add_choice("bx", 0, "") 
    activity = Predicting_YieldingActivity(config, tokenChoices, initialPrompt)
    output = ""
    for s in activity.act():
      output += s
    self.assertEqual(output, "bx")

  def test_predicting_yealding_unfinalized_flat_0_upto_position_0(self):
    config = Configuration(None) # None will use defaults.
    config.predictUptoPosition = 0
    config.tokenizationSeparator = ""
    tokenChoices = TokenChoices()
    tokenChoices.add_choice("a", 0, "b")
    tokenChoices.add_choice("b", 0, "c")
    tokenChoices.add_choice("c", 0, "d")
    initialPrompt = "a"
    activity = Predicting_YieldingActivity(config, tokenChoices, initialPrompt)
    output = ""
    for s in activity.act():
      output += s
    self.assertEqual(output, "bcd") # Even without separator, finalization occurs impilicitly as all tried tokens return the separator when nothing is found.

  def test_predicting_yealding_mix_0_1_2_upto_position_2(self):
    config = Configuration(None) # None will use defaults.
    config.predictUptoPosition = 2
    config.tokenizationSeparator = ""
    tokenChoices = TokenChoices()
    tokenChoices.add_choice("a", 0, "b")
    tokenChoices.add_choice("b", 0, "c")
    tokenChoices.add_choice("c", 0, "d")
    tokenChoices.add_choice("d", 0, "") # Finalization by separator.
    tokenChoices.add_choice("a", 1, "x")
    tokenChoices.add_choice("b", 1, "y")
    tokenChoices.add_choice("c", 1, "z")
    tokenChoices.add_choice("a", 2, "1")
    tokenChoices.add_choice("b", 2, "2")
    tokenChoices.add_choice("c", 2, "3")
    tokenChoices.add_choice("1", 2, "A")
    tokenChoices.add_choice("x1A", 1, "END?")
    initialPrompt = "a"
    activity = Predicting_YieldingActivity(config, tokenChoices, initialPrompt)
    output = ""
    for s in activity.act():
      output += s
    self.assertEqual(output, "bx1AEND?")

