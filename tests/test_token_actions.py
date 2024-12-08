#!/usr/bin/python
import unittest
from pretext.actions import token
from pretext.model.token_graph import TokenGraph

class TestTokenActions(unittest.TestCase):

  def test_model_by_next_1_called_once(self):
    tokens = ["T", "o", "k", "e", "n", "i", "z", "a", "t", "i", "o", "n"]
    tokenGraph = TokenGraph()
    tokenGraph = token.model_by_next(1, tokens, tokenGraph)
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
    # Python doesn't create a list if nothing is found during slicing, which is exactly what we need.
    self.assertEqual(tokenGraph.get_links("x"), [])
    
  def test_model_by_next_1_called_multiple(self):
    # Seemingle redundant links are relevant for statistical analysis; hence, no check for uniqueness when linking.
    tokens = ["1", "2", "3", "2", "1"]
    tokenGraph = TokenGraph()
    tokenGraph = token.model_by_next(1, tokens, tokenGraph)
    tokenGraph = token.model_by_next(1, tokens, tokenGraph)
    self.assertEqual(tokenGraph.get_links("1"), [["2"], ["2"]])
    self.assertEqual(tokenGraph.get_links("2"), [["3"], ["1"], ["3"], ["1"]])
    self.assertEqual(tokenGraph.get_links("3"), [["2"], ["2"]])
    
  def test_model_by_next_3(self):
    # Expected to have links of 3, 2, and 1 step.
    tokens = ["A", "B", "C", "D"]
    tokenGraph = TokenGraph()
    tokenGraph = token.model_by_next(3, tokens, tokenGraph)
    self.assertEqual(tokenGraph.get_links("A"), [["B", "C", "D"]])
    self.assertEqual(tokenGraph.get_links("B"), [["C", "D"]])
    self.assertEqual(tokenGraph.get_links("C"), [["D"]])
    self.assertEqual(tokenGraph.get_links("D"), [])
    
  def test_model_by_next_3_called_multiple(self):
    # Expected to have links of 3, 2, and 1 step.
    tokens = ["A", "B", "C", "D"]
    tokenGraph = TokenGraph()
    tokenGraph = token.model_by_next(3, tokens, tokenGraph)
    tokenGraph = token.model_by_next(3, tokens, tokenGraph)
    self.assertEqual(tokenGraph.get_links("A"), [["B", "C", "D"], ["B", "C", "D"]])
    self.assertEqual(tokenGraph.get_links("B"), [["C", "D"], ["C", "D"]])
    self.assertEqual(tokenGraph.get_links("C"), [["D"], ["D"]])
    self.assertEqual(tokenGraph.get_links("D"), [])
  
  def test_calculate_historgrams(self):
    tokenGraph = TokenGraph()
    tokenGraph.link("A", ["As", "you", "like", "it."])
    tokenGraph.link("C", ["Can't", "do", "it", "better."])
    tokenGraph.link("D", ["Don't", "mention", "it"])
    tokenGraph.link("A", ["Around", "the", "world."])
    tokenGraph.link("C", ["Can't", "think", "of", "anything", "better."])
    tokenGraph.link("D", ["Didn't", "mention", "it"])
    histograms = token.calculate_histograms(tokenGraph)
    self.assertEqual(histograms.get_analysis()["A"][0]["As"], 1)
 #  self.assertEqual(histograms.get_analysis()["A"][1]["As"], None)
    self.assertEqual(histograms.get_analysis()["A"][2]["like"], 1)
    self.assertEqual(histograms.get_analysis()["C"][0]["Can't"], 2)
    self.assertEqual(histograms.get_analysis()["D"][1]["mention"], 2)

  def test_top_of_histogram(self):
    tokenGraph = TokenGraph()
    tokenGraph.link("D", ["Don't", "mention", "it."])
    tokenGraph.link("D", ["Does", "she", "know?"])
    tokenGraph.link("D", ["Didn't", "mention", "it."])
    topOfHistogram = token.top_of_histogram(tokenGraph)
    self.assertEqual(topOfHistogram.get_report()["D"][0], "Don't")
    self.assertEqual(topOfHistogram.get_report()["D"][1], "mention")
    self.assertEqual(topOfHistogram.get_report()["D"][2], "it.")
    
if __name__=="__main__":
  unittest.main() 
