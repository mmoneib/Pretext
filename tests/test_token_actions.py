#!/usr/bin/python
import unittest
import pretext.actions.token as TokenActions # In order for this class to see the main project, pretext was made into a package by adding __init__.py.
#import model.token_graph

class TestTokenActions(unittest.TestCase):

  def test_model_by_next():
    tokens = ["N", "S", "E", "W"]
    tokenGraph = TokenGraph()
    tokenGraph.link("N", ["E", "W"])
    tokenGraph.link("S", ["W", "E"])
    tokenGraph.link("E", ["S", "N"])
    tokenGraph.link("W", ["N", "S"])

if __name__=="__main__":
  unittest.main() 
