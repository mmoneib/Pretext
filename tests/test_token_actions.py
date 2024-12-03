#!/usr/bin/python
import unittest
from pretext.actions import token
from pretext.model.token_graph import TokenGraph

class TestTokenActions(unittest.TestCase):

  def test_model_by_next_called_once(self):
    tokens = ["T", "o", "k", "e", "n", "i", "z", "a", "t", "i", "o", "n"]
    tokenGraph = TokenGraph()
    tokenGraph = token.model_by_next(tokens, tokenGraph)
    # Expected results are lists of lists as to allow for a model where neighborhood is defined by more than one step (modelling by more than 1 next).
    self.assertEqual(tokenGraph.get_links("T"), [["o"]])
    self.assertEqual(tokenGraph.get_links("o"), [["k"],["n"]])
    self.assertEqual(tokenGraph.get_links("k"), [["e"]])
    self.assertEqual(tokenGraph.get_links("n"), [["i"]])
    self.assertEqual(tokenGraph.get_links("i"), [["z"],["o"]])
    self.assertEqual(tokenGraph.get_links("z"), [["a"]])
    self.assertEqual(tokenGraph.get_links("a"), [["t"]])
    self.assertEqual(tokenGraph.get_links("t"), [["i"]])
    self.assertEqual(tokenGraph.get_links("i"), [["z"],["o"]])
    self.assertEqual(tokenGraph.get_links("n"), [["i"]])

if __name__=="__main__":
  unittest.main() 
