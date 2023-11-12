#!/usr/bin/python
import unittest
import pretext # In order for this class to see th main project, pretext was made into a package by adding __init__.py.
from pretext import actions
from pretext.actions import tokenizer

class TestTokenizer(unittest.TestCase):
  def test_tokenize_by_words_2(self):
    self.assertEqual(tokenizer.tokenize_by_words("Apple banana cucumber donuts.", 2), ["Apple banana", "cucumber donuts."])
    self.assertEqual(tokenizer.tokenize_by_words("Apple banana cucumber.", 2), ["Apple banana", "cucumber."])
    self.assertEqual(tokenizer.tokenize_by_words("Apple banana cucumber donuts. Eggs.", 2), ["Apple banana", "cucumber donuts.", "Eggs."])

  def test_tokenize_by_words_3(self):
    self.assertEqual(tokenizer.tokenize_by_words("Apple banana cucumber donuts.", 3), ["Apple banana cucumber", "donuts."])
    self.assertEqual(tokenizer.tokenize_by_words("Apple banana cucumber.", 3), ["Apple banana cucumber."])

if __name__=="__main__":
  unittest.main() 
