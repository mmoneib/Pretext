#!/usr/bin/python
import unittest
from pretext.process.tokenization import TokenizationParallel
from pretext.model.configuration imort Configuration

class TestReadingProcess(unittest.TestCase):

  def test_tokenization_process_single(self):
    config = Configuration()
    tokenization = TokenizationParallel(config)
    
