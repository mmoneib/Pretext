#!/usr/bin/python
import unittest
import pretext.actions.file as FileActions

class TestFileActions(unittest.TestCase):

  def test_read_text_file_single_line(self):
    data = FileActions.read_text_file("tests/resources/test_single_line.txt")
    # Reading a file appends a new-line to the end of the read text.
    self.assertEqual(data, "qwertyuiop\n")

  def test_read_text_file_multi_line(self):
    data = FileActions.read_text_file("tests/resources/test_multi_line.txt")
    # Reading a file appends a new-line to the end of the read text.
    self.assertEqual(data, "asdfghjkl\nzxcvbnm\n")

  def test_read_text_file_end_with_newline(self):
    data = FileActions.read_text_file("tests/resources/test_end_with_newline.txt")
    # Reading a file appends a new-line to the end of the read text.
    self.assertEqual(data, "A\n\n")

  def test_read_text_file_symbols(self): # Mainly to test escaping and supportability.
    data = FileActions.read_text_file("tests/resources/test_symbols.txt")
    # Reading a file appends a new-line to the end of the read text. Double quotation and backspace are escaped by a preceding backspace.
    self.assertEqual(data, "`~!@#$%^&*()_+=-\\';:\"|/.,<>?\n")
