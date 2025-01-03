#!/usr/bin/python
import unittest
from pretext.actions import token
from pretext.archetype.token_graph import TokenGraph
from pretext.archetype.token_choices import TokenChoices

class TestTokenActions(unittest.TestCase):
  tokenizationSeparator = "" # As a variablt to elemenate redundancy and give context.

  def test_append_tokenization_separator(self):
    tokens = ["A", "B", "C"]
    tokens = token.append_tokenization_separator(tokens, self.tokenizationSeparator)
    tokens.extend(["AB", "C"])
    tokens = token.append_tokenization_separator(tokens, self.tokenizationSeparator)
    self.assertEqual(tokens, ["A", "B", "C", "", "AB", "C", self.tokenizationSeparator])

  def test_model_by_next_1_called_once(self):
    tokens = ["T", "o", "k", "e", "n", "i", "z", "a", "t", "i", "o", "n", self.tokenizationSeparator]
    tokenGraph = TokenGraph()
    tokenGraph = token.model_by_next(1, tokens, tokenGraph, self.tokenizationSeparator)
    # Expected results are lists of lists as to allow for a model where neighborhood is defined by more than one step modeling by more than 1 next).
    self.assertEqual(tokenGraph.get_links("T"), [["o"]])
    self.assertEqual(tokenGraph.get_links("o"), [["k"],["n"]])
    self.assertEqual(tokenGraph.get_links("k"), [["e"]])
    self.assertEqual(tokenGraph.get_links("n"), [["i"],[self.tokenizationSeparator]])
    self.assertEqual(tokenGraph.get_links("i"), [["z"],["o"]])
    self.assertEqual(tokenGraph.get_links("z"), [["a"]])
    self.assertEqual(tokenGraph.get_links("a"), [["t"]])
    self.assertEqual(tokenGraph.get_links("t"), [["i"]])
    self.assertEqual(tokenGraph.get_links("i"), [["z"],["o"]])
    self.assertEqual(tokenGraph.get_links("n"), [["i"],[self.tokenizationSeparator]]) # Include "" as separator.
    # Last element should have no entry.
    self.assertEqual(tokenGraph.get_links(self.tokenizationSeparator), [])
    # Python doesn't create a list if nothing is found during slicing, which is exactly what we need.
    self.assertEqual(tokenGraph.get_links("x"), [])

  def test_model_by_next_1_with_separator(self):
    tokens = ["A", "B", "C", self.tokenizationSeparator, "AB", "C", self.tokenizationSeparator]
    tokenGraph = TokenGraph()
    tokenGraph = token.model_by_next(1, tokens, tokenGraph, self.tokenizationSeparator)
    self.assertEqual(tokenGraph.get_links("C"), [[self.tokenizationSeparator], [self.tokenizationSeparator]])
    # Separator should have no links.
    self.assertEqual(tokenGraph.get_links(self.tokenizationSeparator), [])
    
  def test_model_by_next_1_called_multiple(self):
    # Seemingle redundant links are relevant for statistical analysis; hence, no check for uniqueness when linking.
    tokens = ["1", "2", "3", "2", "1"]
    tokenGraph = TokenGraph()
    tokenGraph = token.model_by_next(1, tokens, tokenGraph, self.tokenizationSeparator)
    tokenGraph = token.model_by_next(1, tokens, tokenGraph, self.tokenizationSeparator)
    self.assertEqual(tokenGraph.get_links("1"), [["2"], ["2"]])
    self.assertEqual(tokenGraph.get_links("2"), [["3"], ["1"], ["3"], ["1"]])
    self.assertEqual(tokenGraph.get_links("3"), [["2"], ["2"]])
    
  def test_model_by_next_3(self):
    # Expected to have links of 3, 2, and 1 step.
    tokens = ["A", "B", "C", "D"]
    tokenGraph = TokenGraph()
    tokenGraph = token.model_by_next(3, tokens, tokenGraph, self.tokenizationSeparator)
    self.assertEqual(tokenGraph.get_links("A"), [["B", "C", "D"]])
    self.assertEqual(tokenGraph.get_links("B"), [["C", "D"]])
    self.assertEqual(tokenGraph.get_links("C"), [["D"]])
    self.assertEqual(tokenGraph.get_links("D"), [])
    
  def test_model_by_next_3_called_multiple(self):
    # Expected to have links of 3, 2, and 1 step.
    tokens = ["A", "B", "C", "D"]
    tokenGraph = TokenGraph()
    tokenGraph = token.model_by_next(3, tokens, tokenGraph, self.tokenizationSeparator)
    tokenGraph = token.model_by_next(3, tokens, tokenGraph, self.tokenizationSeparator)
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
    self.assertEqual(histograms.get_scores()["A"][0]["As"], 1)
 #  self.assertEqual(histograms.get_scores()["A"][1]["As"], None)
    self.assertEqual(histograms.get_scores()["A"][2]["like"], 1)
    self.assertEqual(histograms.get_scores()["C"][0]["Can't"], 2)
    self.assertEqual(histograms.get_scores()["D"][1]["mention"], 2)

  def test_top_of_histogram(self):
    tokenGraph = TokenGraph()
    tokenGraph.link("D", ["Don't", "mention", "it."])
    tokenGraph.link("D", ["Does", "she", "know?"])
    tokenGraph.link("D", ["Didn't", "mention", "it."])
    topOfHistogram = token.top_of_histogram(tokenGraph)
    self.assertEqual(topOfHistogram.get_choices()["D"][0], "Don't")
    self.assertEqual(topOfHistogram.get_choices()["D"][1], "mention")
    self.assertEqual(topOfHistogram.get_choices()["D"][2], "it.")
    
  # Optimistic and pessimistic evaluation of tokens should behave the same if there are no valid predictions before the agreement point between both opposite directions.
  def test_predict_position_0_exact_token(self):
    tokenChoices = TokenChoices()
    tokenChoices.add_choice("As fa", 0, "r")
    tokenChoices.add_choice("Tomorrow never", 0, " dies.")
    token1 = "As fa"
    token2 = "Tomorrow never"
    prediction1 = token.predict_optimistically(tokenChoices, token1, 0, self.tokenizationSeparator)
    prediction2 = token.predict_optimistically(tokenChoices, token2, 0, self.tokenizationSeparator)
    prediction3 = token.predict_pessimistically(tokenChoices, token1, 0, self.tokenizationSeparator)
    prediction4 = token.predict_pessimistically(tokenChoices, token2, 0, self.tokenizationSeparator)
    self.assertEqual(prediction1, "r")
    self.assertEqual(prediction2, " dies.")
    self.assertEqual(prediction3, "r")
    self.assertEqual(prediction4, " dies.")
    
  def test_predict_position_1_exact_token(self):
    tokenChoices = TokenChoices()
    tokenChoices.add_choice("As fa", 0, "r")
    tokenChoices.add_choice("As fa", 1, " ")
    tokenChoices.add_choice("Tomorrow never", 0, " dies.")
    tokenChoices.add_choice("Tomorrow never", 1, " Nevertheless,")
    token1 = "As fa"
    token2 = "Tomorrow never"
    prediction1 = token.predict_optimistically(tokenChoices, token1, 1, self.tokenizationSeparator)
    prediction2 = token.predict_optimistically(tokenChoices, token2, 1, self.tokenizationSeparator)
    prediction3 = token.predict_pessimistically(tokenChoices, token1, 1, self.tokenizationSeparator)
    prediction4 = token.predict_pessimistically(tokenChoices, token2, 1, self.tokenizationSeparator)
    self.assertEqual(prediction1, "r ")
    self.assertEqual(prediction2, " dies. Nevertheless,")
    self.assertEqual(prediction3, "r ")
    self.assertEqual(prediction4, " dies. Nevertheless,")
    
  def test_predict_position_1_partial(self):
    tokenChoices = TokenChoices()
    tokenChoices.add_choice("As fa", 0, "r")
    tokenChoices.add_choice("As fa", 1, " ")
    tokenChoices.add_choice("Tomorrow never", 0, " dies.")
    tokenChoices.add_choice("Tomorrow never", 1, " Nevertheless,")
    token1 = "known. As fa"
    token2 = "yesterday. Tomorrow never"
    prediction1 = token.predict_optimistically(tokenChoices, token1, 1, self.tokenizationSeparator)
    prediction2 = token.predict_optimistically(tokenChoices, token2, 1, self.tokenizationSeparator)
    prediction3 = token.predict_pessimistically(tokenChoices, token1, 1, self.tokenizationSeparator)
    prediction4 = token.predict_pessimistically(tokenChoices, token2, 1, self.tokenizationSeparator)
    self.assertEqual(prediction1, "r ")
    self.assertEqual(prediction2, " dies. Nevertheless,")
    self.assertEqual(prediction3, "r ")
    self.assertEqual(prediction4, " dies. Nevertheless,")
    
  def test_predict_position_beyond_available(self):
    tokenChoices = TokenChoices()
    tokenChoices.add_choice("As fa", 0, "r")
    token1 = "As fa"
    prediction1 = token.predict_optimistically(tokenChoices, token1, 3, self.tokenizationSeparator)
    prediction2 = token.predict_pessimistically(tokenChoices, token1, 3, self.tokenizationSeparator)
    self.assertEqual(prediction1, "r")
    self.assertEqual(prediction2, "r")

  def test_predict_position_0_finalization(self):
    tokenChoices = TokenChoices()
    tokenChoices.add_choice("BCD", 0, "3")
    tokenChoices.add_choice("KLM", 0, self.tokenizationSeparator) # Finalization.
    tokenChoices.add_choice("LM", 0, "2")
    tokenChoices.add_choice("Z", 0, "1")
    token1 = "ABCD"
    token2 = "JKLM"
    token3 = "WXYZ"
    prediction1 = token.predict_optimistically(tokenChoices, token1, 0, self.tokenizationSeparator)
    prediction2 = token.predict_optimistically(tokenChoices, token2, 5, self.tokenizationSeparator)
    prediction3 = token.predict_optimistically(tokenChoices, token3, 3, self.tokenizationSeparator)
    prediction4 = token.predict_pessimistically(tokenChoices, token1, 0, self.tokenizationSeparator)
    prediction5 = token.predict_pessimistically(tokenChoices, token2, 5, self.tokenizationSeparator)
    prediction6 = token.predict_pessimistically(tokenChoices, token3, 3, self.tokenizationSeparator)
    self.assertEqual(prediction1, "3")
    self.assertEqual(prediction2, self.tokenizationSeparator)
    self.assertEqual(prediction3, "1")
    self.assertEqual(prediction4, "3")
    self.assertEqual(prediction5, "2") # TODO Different the optimistic. Highlight difference between flows in a separate test.
    self.assertEqual(prediction6, "1")

  def test_predict_position_0_not_found(self):
    tokenChoices = TokenChoices()
    tokenChoices.add_choice("A", 0, "1")
    token1 = "X"
    prediction1 = token.predict_optimistically(tokenChoices, token1, 0, self.tokenizationSeparator)
    prediction2 = token.predict_pessimistically(tokenChoices, token1, 0, self.tokenizationSeparator)
    self.assertEqual(prediction1, self.tokenizationSeparator)
    self.assertEqual(prediction2, self.tokenizationSeparator)
    
if __name__=="__main__":
  unittest.main() 
