#!/usr/bin/python
import unittest
import queue
import threading
import multiprocessing
import concurrent.futures
import pretext.activity.tokenization as tokenization # Needed for ProcessPoolExecutor
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
  def test_tokenization_activity_parallel_using_multiprocessing_with_queue(self):
    self._run_2_tokenization_tasks_in_parallel_with_worker_queue(multiprocessing.Process, multiprocessing.Queue())

  ## Tests tokenization running 2 processes in parallel and retrieve the results using a worker queue.
  def test_tokenization_activity_parallel_using_threading_with_queue(self):
    self._run_2_tokenization_tasks_in_parallel_with_worker_queue(threading.Thread, queue.Queue()) 

  ## A generic function to define the worker and initiate the tasks for threads and processes testing using a worker queue. A proof that the application can be configured to run either using threads or processes. When choosing, threading is good for tasks of long waiting time that the overall runtime would benefit from context switching; while processess provide better performance for concurrent tasks if the separate memory spaces overhead is not an issue.
  def _run_2_tokenization_tasks_in_parallel_with_worker_queue(self, parallelizationClass, qu):
    # Use configuration defaults.
    config = Configuration(None) # None will use defaults.
    # Override configuration defaults.
    config.charsTokenizationSteps = [1,2]
    config.wordsTokenizationSteps = [1,2]
    # Define worker.
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

  def test_tokenization_activity_parallel_using_futures_thread_pool_executor(self):
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
    self._run_2_tokenization_tasks_in_parallel_with_executor(executor)
 
  def test_tokenization_activity_parallel_using_futures_process_pool_executor(self):
    executor = concurrent.futures.ProcessPoolExecutor(max_workers=2)
    self._run_2_tokenization_tasks_in_parallel_with_executor(executor)

  def test_tokenization_activity_parallel_using_multiprocessing_pool_executor(self):
    executor = multiprocessing.Pool(processes=2)
    self._run_2_tokenization_tasks_in_parallel_with_executor(executor)

  ## A generic function to define the worker and initiate the tasks for threads and processes testing using an executor. 
  def _run_2_tokenization_tasks_in_parallel_with_executor(self, executor):
    config = Configuration(None) # None will use defaults.	
    config.charsTokenizationSteps = [1,2]
    config.wordsTokenizationSteps = [1,2]
    activities = []
    activities.append(Tokenization_ParallelActivity(config, "ABCD"))
    activities.append(Tokenization_ParallelActivity(config, "QWER"))
    with executor as executor:
      # list(...) to cast from iterable, map(...) for ordered executions. Otherwise, submit(...).
      # lambda could be used instead of named function for threads. For processes, however, it fails being local to a class.
      output = list(executor.map(tokenization.get_task_output, activities))
    self.assertEqual(output[0], ["A","B","C","D","AB","CD","ABCD","ABCD"])
    self.assertEqual(output[1], ["Q","W","E","R","QW","ER","QWER","QWER"])

