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

  def test_reading_prcoess_multiple_file(self):
    fileNames = ["tests/resources/test_end_with_newline.txt", "tests/resources/test_multi_line.txt", "tests/resources/test_single_line.txt", "tests/resources/test_symbols.txt"]
    process = ReadingYieldingProcess(fileNames)
    text = ""
    for fileText in  process.process():
      text += fileText
    self.assertEqual(text, "A\n\nasdfghjkl\nzxcvbnm\nqwertyuiop\n`~!@#$%^&*()_+=-\\';:\"|/.,<>?\n")
