#!/usr/bin/python
import unittest
import queue
import threading
import multiprocessing
from pretext.activity.tokenization import Tokenization_ParallelActivity
from pretext.archetype.configuration import Configuration

class TestTokenizationActivity(unittest.TestCase):

  ## Tests tokenization using 2 threads run in a bare bone way without a queue, taking advantage of the shared memory space with the main thread.
  def test_tokenization_activity_parallel_using_threading_without_queue(self):
    config = Configuration(None) # None will use defaults.
    # Override configuration defaults.
    config.charsTokenizationSteps = [1,2]
    config.wordsTokenizationSteps = [1,2]
    # Create instances.
    tokenization1 = Tokenization_ParallelActivity(config, "ABCD")
    tokenization2 = Tokenization_ParallelActivity(config, "QWER")
    # Create processes.
    tokenizationTask1 = threading.Thread(target=tokenization1.act)
    tokenizationTask2 = threading.Thread(target=tokenization2.act)
    # Start threads.
    tokenizationTask1.start()
    tokenizationTask2.start()
    # Wait for threads' act() function to finish. In 'blocking' mode, that's when the output would be ready for retrieval.
    tokenizationTask1.join()
    tokenizationTask2.join()
    # Retrieve the output from the instances. This is possible without affecting the parallelization because ouptut() is separated from act().
    self.assertEqual(tokenization1.output(), ["A","B","C","D","AB","CD","ABCD","ABCD"])
    self.assertEqual(tokenization2.output(), ["Q","W","E","R","QW","ER","QWER","QWER"])
    
  ## Tests tokenization running 2 threads in paralllel and retrieve the results using a worker queue.
  def test_tokenization_activity_parallel_using_multiprocessing(self):
    self._run_2_tokenization_tasks_in_parallel_with_worker_queue(multiprocessing.Process, multiprocessing.Queue())

  ## Tests tokenization running 2 processes in paralllel and retrieve the results using a worker queue.
  def test_tokenization_activity_parallel_using_threading_with_queue(self):
    self._run_2_tokenization_tasks_in_parallel_with_worker_queue(threading.Thread, queue.Queue()) 

  ## A generic function to define the worker and initiate the tasks for threads and processes testing. A proof that the application can be configured to run either using threads or processes.
  def _run_2_tokenization_tasks_in_parallel_with_worker_queue(self, parallelizationClass, qu):
    config = Configuration(None) # None will use defaults.
    # Override configuration defaults.
    config.charsTokenizationSteps = [1,2]
    config.wordsTokenizationSteps = [1,2]
    def worker(self, qu, text): # Not using 'queue' to emphasize the different context.
      instance = Tokenization_ParallelActivity(config, text)
      qu.put(instance.act().output()) # Chain of commands.
    # Create processes.
    tokenizationTask1 = parallelizationClass(target=worker, args=(1, qu, "ABCD"))
    tokenizationTask2 = parallelizationClass(target=worker, args=(2, qu, "QWER"))
    # Start threads.
    tokenizationTask1.start()
    tokenizationTask2.start()
    # Wait for threads' act() function to finish. In 'blocking' mode, that's when the output would be ready for retrieval.
    tokenizationTask1.join()
    tokenizationTask2.join()
    # Retrieve the output from the instances. This is possible without affecting the parallelization because ouptut() is separated from act().
    self.assertEqual(qu.get(), ["A","B","C","D","AB","CD","ABCD","ABCD"])
    self.assertEqual(qu.get(), ["Q","W","E","R","QW","ER","QWER","QWER"])

