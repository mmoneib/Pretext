#!/usr/bin/python
import unittest
import pretext.actions.file as FileActions

class TestFileActions(unittest.TestCase):

  def test_read_text_file(self):
    data = FileActions.read_text_file("tests/resources/test.txt")
    # Reading a file appends a new-line to the end of the read text.
    self.assertEqual(data, "qwertyuiop\n")

