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
  # Same inputs conceptually because we are testing integration of tasks rather than the tokenizaiton action itself.
  input1 = "ABCD"
  input2 = "QWER"
  separator = ""
  #TODO Are the repitition in the last 4 tokens problematic? One is 1 word tokenization and the other is for 2 words.
  expectedOutput1 = ["A","B","C","D",separator,"AB","CD",separator,"ABCD","","ABCD",separator]
  expectedOutput2 = ["Q","W","E","R",separator,"QW","ER",separator,"QWER","","QWER",separator]
    
  ## Tests tokenization using 2 threads run in a bare bone way without a queue, taking advantage of the shared memory space with the main thread.
  def test_tokenization_activity_parallel_using_threading_without_queue(self):
    config = Configuration(None) # None will use defaults.
    # Override configuration defaults.
    config.charsTokenizationSteps = [1,2]
    config.wordsTokenizationSteps = [1,2]
    # Create instances.
    tokenization1 = Tokenization_ParallelActivity(config, self.input1)
    tokenization2 = Tokenization_ParallelActivity(config, self.input2)
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
    self.assertEqual(tokenization1.output(), self.expectedOutput1)
    self.assertEqual(tokenization2.output(), self.expectedOutput2)
    
  ## Tests tokenization running 2 threads in paralllel and retrieve the results using a worker queue.
  def test_tokenization_activity_parallel_using_multiprocessing_with_queue(self):
    self._run_2_tokenization_tasks_in_parallel_with_worker_queue(multiprocessing.Process, multiprocessing.Queue())

  ## Tests tokenization running 2 processes in parallel and retrieve the results using a worker queue.
  def test_tokenization_activity_parallel_using_threading_with_queue(self):
    self._run_2_tokenization_tasks_in_parallel_with_worker_queue(threading.Thread, queue.Queue()) 

  ## A generic function to define the worker and initiate the tasks for threads and processes testing using a worker queue. A proof that the application can be configured to run either using threads or processes. When choosing, threading is good for tasks of long waiting time that the overall runtime would benefit from context switching; while processess provide better performance for concurrent tasks if the separate memory spaces overhead is not an issue.
  def _run_2_tokenization_tasks_in_parallel_with_worker_queue(self, parallelizationClass, qu): # Not 'queue' as it is a module's name.
    # Use configuration defaults.
    config = Configuration(None) # None will use defaults.
    # Override configuration defaults.
    config.charsTokenizationSteps = [1,2]
    config.wordsTokenizationSteps = [1,2]
    # Define worker.
    def worker(self, q, text): # Not using 'qu' to emphasize the different context.
      instance = Tokenization_ParallelActivity(config, text)
      q.put(instance.act().output()) # Chain of commands.
    # Create processes.
    tokenizationTask1 = parallelizationClass(target=worker, args=(1, qu, self.input1))
    tokenizationTask2 = parallelizationClass(target=worker, args=(2, qu, self.input2))
    # Start threads.
    tokenizationTask1.start()
    tokenizationTask2.start()
    # Wait for threads' act() function to finish. In 'blocking' mode, that's when the output would be ready for retrieval.
    tokenizationTask1.join()
    tokenizationTask2.join()
    # Retrieve the output from the instances. This is possible without affecting the parallelization because ouptut() is separated from act().
    self.assertEqual(qu.get(), self.expectedOutput1)
    self.assertEqual(qu.get(), self.expectedOutput2)

  def test_tokenization_activity_parallel_using_futures_thread_pool_executor(self):
    chosenExecutor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
    self._run_2_tokenization_tasks_in_parallel_with_executor(chosenExecutor)
 
  def test_tokenization_activity_parallel_using_futures_process_pool_executor(self):
    chosenExecutor = concurrent.futures.ProcessPoolExecutor(max_workers=2)
    self._run_2_tokenization_tasks_in_parallel_with_executor(chosenExecutor)

  def test_tokenization_activity_parallel_using_multiprocessing_pool_executor(self):
    chosenExecutor = multiprocessing.Pool(processes=2)
    self._run_2_tokenization_tasks_in_parallel_with_executor(chosenExecutor)

  def test_tokenization_activity_parallel_using_multiprocessing_pool_executor_async(self):
    chosenExecutor = concurrent.futures.ProcessPoolExecutor(max_workers=2)
    self._run_2_tokenization_tasks_in_parallel_with_executor(chosenExecutor, False)

  ## A generic function to define the worker and initiate the tasks for threads and processes testing using an executor. 
  def _run_2_tokenization_tasks_in_parallel_with_executor(self, chosenExecutor, isSync=True):
    config = Configuration(None) # None will use defaults.	
    config.charsTokenizationSteps = [1,2]
    config.wordsTokenizationSteps = [1,2]
    activities = []
    activities.append(Tokenization_ParallelActivity(config, self.input1))
    activities.append(Tokenization_ParallelActivity(config, self.input2))
    with chosenExecutor as executor:
      if isSync:
        # list(...) to cast from iterable. Using map(...) for synchronous, ordered executions, returns an iterable including all outputs. The called control the timing and the caller blocks.
        # lambda could be used instead of named function for threads. For processes, however, it fails being local to a class.
        output = list(executor.map(tokenization.get_task_output, activities))
        output = list(executor.map(tokenization.get_task_output, activities))
      else:
        # Using submit for asynchronous, maybe unordered executions, return a future per tasl from which the output can be retrieved. The caller controls the timing.
        future1 = executor.submit(tokenization.get_task_output, activities[0])
        future2 = executor.submit(tokenization.get_task_output, activities[1])
        output = [future1.result(timeout=2), future2.result(timeout=2)]
    self.assertEqual(output[0], self.expectedOutput1)
    self.assertEqual(output[1], self.expectedOutput2)

  def test_tokenization_activity_with_non_consecutive_steps(self):
    config = Configuration(None) # None will use defaults.	
    config.charsTokenizationSteps = [2]
    config.wordsTokenizationSteps = [2]
    activity1 = Tokenization_ParallelActivity(config, self.input1)
    activity2 = Tokenization_ParallelActivity(config, self.input2)
    thisExpectedOutput1 = ["AB","CD",self.separator,"ABCD",""]
    thisExpectedOutput2 = ["QW","ER",self.separator,"QWER",""]
    self.assertEqual(activity1.act().output(), thisExpectedOutput1)
    self.assertEqual(activity2.act().output(), thisExpectedOutput2)

