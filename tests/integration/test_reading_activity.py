#!/usr/bin/python
import unittest
from pretext.activity.reading import Reading_YieldingActivity
from pretext.archetype.configuration import Configuration

class TestReadingActivity(unittest.TestCase):

  def test_reading_activity_single_file(self):
    config = Configuration(None)
    config.commonWordReplacement = None
    fileName = ["tests/resources/test_multi_line.txt"]
    activity = Reading_YieldingActivity(config, fileName)
    text = ""
    for fileText in  activity.act():
      text += fileText
    self.assertEqual(text, "asdfghjkl\nzxcvbnm\n")

  def test_reading_activity_multiple_file(self):
    config = Configuration(None)
    config.commonWordReplacement = None
    fileNames = ["tests/resources/test_end_with_newline.txt", "tests/resources/test_multi_line.txt", "tests/resources/test_single_line.txt", "tests/resources/test_symbols.txt"]
    activity = Reading_YieldingActivity(config, fileNames)
    text = ""
    for fileText in  activity.act():
      text += fileText
    self.assertEqual(text, "A\n\nasdfghjkl\nzxcvbnm\nqwertyuiop\n`~!@#$%^&*()_+=-\\';:\"|/.,<>?\n")
