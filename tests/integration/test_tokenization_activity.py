#!/usr/bin/python
import unittest
from pretext.activity.tokenization import Tokenization_ParallelActivity
from pretext.archetype.configuration import Configuration

class TestReadingProcess(unittest.TestCase):

  def test_tokenization_activity_single(self):
    config = Configuration(None)
    
    tokenization = Tokenization_ParallelActivity(config, "")
    
