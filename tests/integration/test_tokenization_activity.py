#!/usr/bin/python
import unittest
import threading
from pretext.activity.tokenization import Tokenization_ParallelActivity
from pretext.archetype.configuration import Configuration

class TestReadingProcess(unittest.TestCase):

  def test_tokenization_activity_parallel_using_threading(self):
    config = Configuration(None) # None will use defaults.
    # Override configuration defaults.
    config.charsTokenizationSteps = [1,2]
    config.wordsTokenizationSteps = [1,2]
    # Create instances.
    tokenization1 = Tokenization_ParallelActivity(config, "ABCD")
    tokenization2 = Tokenization_ParallelActivity(config, "QWER")
    # Create threads.
    tokenizationTask1 = threading.Thread(target=tokenization1.act())
    tokenizationTask2 = threading.Thread(target=tokenization2.act())
    # Start threads.
    tokenizationTask1.start()
    tokenizationTask2.start()
    # Wait for threads' act() function to finish. In 'blocking' mode, that's when the output would be reade for retrieval.
    tokenizationTask1.join()
    tokenizationTask2.join()
    # Retrieve the output from the instances.
    self.assertEqual(len(tokenization1.output()) == 8, True)
    self.assertEqual(len(tokenization2.output()) == 8, True)
