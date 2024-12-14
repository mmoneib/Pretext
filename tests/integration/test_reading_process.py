#!/usr/bin/python
import unittest
from pretext.process.reading import ReadingYieldingProcess

class TestReadingProcess(unittest.TestCase):

  def test_reading_prcoess_single_file(self):
    fileName = ["tests/resources/test_multi_line.txt"]
    process = ReadingYieldingProcess(fileName)
    text = ""
    for fileText in  process.process():
      text += fileText
    self.assertEqual(text, "asdfghjkl\nzxcvbnm\n")
