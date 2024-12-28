#!/usr/bin/python
import unittest
from pretext.activity.predicting import Predicting_YieldingActivity
from pretext.archetype.configuration import Configuration
from pretext.archetype.token_choices import TokenChoices

class TestPredictingActivity(unittest.TestCase):

  def test_predicting_yealding(self):
    config = Configuration(None) # None will use defaults.
    config.predictUptoPosition = 1
    #tokenChoices = {"a": ["b"], "b": ["c"], "c": ["d"]}
    tokenChoices = TokenChoices()
    tokenChoices.add_choice("a", 0, "b")
    tokenChoices.add_choice("b", 0, "c")
    tokenChoices.add_choice("c", 0, "d")
    tokenChoices.add_choice("d", 0, "")
    initialPrompt = "a"
    activity = Predicting_YieldingActivity(config, tokenChoices, initialPrompt)
    output = ""
    for s in activity.act():
      output += s
    self.assertEqual(output, "bcd")
