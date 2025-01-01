#!/usr/bin/python
import unittest
import queue
import threading
import multiprocessing
from pretext.activity.modeling import Modeling_ParallelActivity
from pretext.archetype.configuration import Configuration
from pretext.archetype.token_graph import TokenGraph

# For more tests of parallelization flavoes, see TestTokenizationActivity
class TestModelingActivity(unittest.TestCase):
    
  ## Tests modeling running 2 threads in paralllel and retrieve the results using a worker queue.
  def test_modeling_activity_parallel_using_multiprocessing_with_queue(self):
    self._run_2_modeling_tasks_in_parallel_with_worker_queue(multiprocessing.Process, multiprocessing.Queue())

  ## Tests modeling running 2 processes in parallel and retrieve the results using a worker queue.
  def test_modeling_activity_parallel_using_threading_with_queue(self):
    self._run_2_modeling_tasks_in_parallel_with_worker_queue(threading.Thread, queue.Queue()) 

  def _run_2_modeling_tasks_in_parallel_with_worker_queue(self, parallelizationClass, queue):
    # Use configuration defaults.
    config = Configuration(None) # None will use defaults.
    config.numOfNextTokens = 1
    # Override configuration defaults.
    pass
    # Define worker.
    def worker(self, qu, tokens, tokenGraph): # Not using 'queue' to emphasize the different context.
      instance = Modeling_ParallelActivity(config, tokens, tokenGraph)
      qu.put(instance.act().output()) # Chain of commands.
    # Create processes.
    modelingTask1 = parallelizationClass(target=worker, args=(1, queue, ["A","B","C","D","","AB","CD","","ABCD","","ABCD",""], TokenGraph()))
    modelingTask2 = parallelizationClass(target=worker, args=(2, queue, ["Q","W","E","R","","QW","ER","","QWER","","QWER",""], TokenGraph()))
    # Start threads.
    modelingTask1.start()
    modelingTask2.start()
    # Wait for threads' act() function to finish. In 'blocking' mode, that's when the output would be ready for retrieval.
    modelingTask1.join()
    modelingTask2.join()
    # Retrieve the output from the instances. This is possible without affecting the parallelization because ouptut() is separated from act().
    self.assertEqual(queue.get().get_graph(), [("A", ["B"]),("B", ["C"]),("C", ["D"]),("D", [""]),("AB", ["CD"]),("CD", [""]),("ABCD", [""]),("ABCD", [""])])
    self.assertEqual(queue.get().get_graph(), [("Q", ["W"]),("W", ["E"]),("E", ["R"]),("R", [""]),("QW", ["ER"]),("ER", [""]),("QWER", [""]),("QWER", [""])])

