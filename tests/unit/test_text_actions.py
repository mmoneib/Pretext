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

  def test_tokenize_by_words_2(self):
    self.assertEqual(TextActions.tokenize_by_words("Apple banana cucumber donuts.", 2), ["Apple banana", " cucumber donuts."])
    self.assertEqual(TextActions.tokenize_by_words("Apple banana cucumber.", 2), ["Apple banana", " cucumber."])
    self.assertEqual(TextActions.tokenize_by_words("Apple banana cucumber donuts. Eggs.", 2), ["Apple banana", " cucumber donuts.", " Eggs."])

  def test_tokenize_by_words_3(self):
    self.assertEqual(TextActions.tokenize_by_words("Apple banana cucumber donuts.", 3), ["Apple banana cucumber", " donuts."])
    self.assertEqual(TextActions.tokenize_by_words("Apple banana cucumber.", 3), ["Apple banana cucumber."])

if __name__=="__main__":
  unittest.main() 
