# Pretext
A text predictor based on statistical inference.

## Structure
Entry script is separated from library to ease relative imports within the library so as to reconcile script and test importing (both assuming 'pretext' as a separate module), as well as publishing of the library. The logic behind the modules within the library follows an _action-archetype-activity_ model of separation in which _actions_ include the building-blocks of the business model, _archetype_ includes the data structures, and _activity_ allow for modular management of chunks of _actions_. Hence, _archetype_ should only be accessed by _actions_, and _actions_ should be only accessed by _activity_.

Structure is as follows:

root (script, license, readme)
|
|
-- pretext (library)
|    |
|    |
|    -- actions (static, utitlity functions)
|    |
|    |
|    -- archetype (data structures)
|    |
|    |
|    -- activity (modular managers of actions)
|    |
|    |
|    -- assemblage (framework of execution, managing activities)
|
|
-- tests
     |
     |
     -- unit (tests of actions layer)
     |
     |
     -- integration (tests of activity layer)

## More on Structure
* Actions are grouped based on their prominent archetype.
* Ideally, an action should be lacking business context as it can be used by different activities, ore even application.
* Assemblage includes all parallelization and organization efforts of activities.

## Run
Run _python pretext.py_ to see the usage template, or run _pythin pretext,py -h_ to get the detailed help.
### Example - Learning from Specific Files: _python pretext.py --knowledge-files pretext.py pretext/actions/token.py_
### Example - Learning from Specific Files in Directory: _python pretext.py --knowledge-files ~/Documents/\*__
### Example - Learning with Custom Tokenization: _python pretext.py -k pretext.py pretext/actions/token.py -w 3 6 -c 11 21 31_
### Example - Learning with Prompt for Prediction: _python pretext.py --knowledge-files pretext.py pretext/actions/token.py -p "Arti"_ 

## Test
Running all tests: _python -m unittest discover tests_

Running a specific test component: _python -m unittest test_module_qulaified_path_here_
### Example: _python -m unittest tests.unit.test_text_actions_
### Example: _python -m unittest tests.unit.test_text_actions.TestTokenActions.test_tokenize_by_words_3_
