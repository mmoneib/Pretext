#!/usr/bin/python
import unittest
import pretext.actions.text as TextActions # In order for this class to see the main project, pretext was made into a package by adding __init__.py.

class TestTextActions(unittest.TestCase):

  def test_tokenize_by_chars_1(self):
    self.assertEqual(TextActions.tokenize_by_chars("AaBbCcDd", 1), ['A', 'a', 'B', 'b', 'C', 'c', 'D', 'd'])
    self.assertEqual(TextActions.tokenize_by_chars("AaBbCcDd", 2), ['Aa', 'Bb', 'Cc', 'Dd'])
    self.assertEqual(TextActions.tokenize_by_chars("AaBbCcDd", 3), ['AaB', 'bCc', 'Dd'])
    self.assertEqual(TextActions.tokenize_by_chars("X", 3), ['X'])
    self.assertEqual(TextActions.tokenize_by_chars("X", 1), ['X'])

  def test_tokenize_by_words_1(self):
    self.assertEqual(TextActions.tokenize_by_words("Apple banana cucumber donuts.", 1), ["Apple", " banana", " cucumber", " donuts."])
    self.assertEqual(TextActions.tokenize_by_words("Apple banana cucumber.", 1), ["Apple", " banana", " cucumber."])
    self.assertEqual(TextActions.tokenize_by_words("Apple banana cucumber donuts. Eggs.", 1), ["Apple", " banana", " cucumber", " donuts.", " Eggs."])
    self.assertEqual(TextActions.tokenize_by_words("Apple.", 1), ["Apple."])

  def test_tokenize_by_words_2(self):
    self.assertEqual(TextActions.tokenize_by_words("Apple banana cucumber donuts.", 2), ["Apple banana", " cucumber donuts."])
    self.assertEqual(TextActions.tokenize_by_words("Apple banana cucumber.", 2), ["Apple banana", " cucumber."])
    self.assertEqual(TextActions.tokenize_by_words("Apple banana cucumber donuts. Eggs.", 2), ["Apple banana", " cucumber donuts.", " Eggs."])
    self.assertEqual(TextActions.tokenize_by_words("Apple.", 2), ["Apple."])

  def test_tokenize_by_words_3(self):
    self.assertEqual(TextActions.tokenize_by_words("Apple banana cucumber donuts.", 3), ["Apple banana cucumber", " donuts."])
    self.assertEqual(TextActions.tokenize_by_words("Apple banana cucumber.", 3), ["Apple banana cucumber."])

  def test_remove_common_words_non_empty(self):
    commonWordReplacement = "§"
    self.assertEqual(TextActions.remove_common_words("Apple banana the donuts.", commonWordReplacement), "Apple banana §donuts.")
    self.assertEqual(TextActions.remove_common_words("in the of", commonWordReplacement), "in §of")
    self.assertEqual(TextActions.remove_common_words("am in the of", commonWordReplacement), "am §§of")
    self.assertEqual(TextActions.remove_common_words("breathe the air", commonWordReplacement), "breathe §air")
    self.assertEqual(TextActions.remove_common_words("ongoing destruction offending their forward looking roof", commonWordReplacement), "ongoing destruction offending their forward looking roof") # Common words within words should not be affected.

  def test_remove_common_words_empty(self):
    commonWordReplacement = ""
    self.assertEqual(TextActions.remove_common_words("Apple banana the donuts.", commonWordReplacement), "Apple banana donuts.")
    self.assertEqual(TextActions.remove_common_words("in the of", commonWordReplacement), "in of")
    self.assertEqual(TextActions.remove_common_words("am in the of", commonWordReplacement), "am of")
    self.assertEqual(TextActions.remove_common_words("breathe the air", commonWordReplacement), "breathe air")
    self.assertEqual(TextActions.remove_common_words("ongoing destruction offending their forward looking roof", commonWordReplacement), "ongoing destruction offending their forward looking roof") 

  def test_remove_common_words_space(self):
    commonWordReplacement = " "
    self.assertEqual(TextActions.remove_common_words("Apple banana the donuts.", commonWordReplacement), "Apple banana donuts.")
    self.assertEqual(TextActions.remove_common_words("in the of", commonWordReplacement), "in of")
    self.assertEqual(TextActions.remove_common_words("am in the of", commonWordReplacement), "am of")
    commonWordReplacement = "  "
    self.assertEqual(TextActions.remove_common_words("breathe the air", commonWordReplacement), "breathe  air")
    self.assertEqual(TextActions.remove_common_words("ongoing destruction offending their forward looking roof", commonWordReplacement), "ongoing destruction offending their forward looking roof") 

  def test_count_words(self):
    self.assertEqual(TextActions.count_words("A B"), 2)
    self.assertEqual(TextActions.count_words("A  cat IN     the		hat."), 5)

if __name__=="__main__":
  unittest.main() 
