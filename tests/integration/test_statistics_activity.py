#!/usr/bin/python
import unittest
from pretext.activity.statistics import Statistics_ProceduralActivity
from pretext.archetype.token_graph import TokenGraph

class TestStatisticsActivity(unittest.TestCase):

  def test_statistics_activity(self):
    tokenGraph = TokenGraph()
    tokenGraph.link("I", ["can't", "stand", "anything."])
    tokenGraph.link("I", ["can"])
    tokenGraph.link("I", ["can", "do", "it."])
    tokenGraph.link("I", ["can", "do", "anything"])
    tokenGraph.link("He", ["can't", "do", "it."])
    tokenGraph.link("He", ["can't", "track", "it."])
    tokenGraph.link("He", ["can't", "see", "it."])
    tokenGraph.link("He", ["can't", "see", "him."])
    activity = Statistics_ProceduralActivity(tokenGraph)
    activity.act()
    self.assertEqual(activity.output().get_choices(), {"I": ["can", "do", "anything."],"He": ["can't", "see", "it."]})
