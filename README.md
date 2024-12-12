# Pretext
A text predictor based on statistical inference.

## Structure
Entry script is separated from library to ease relative imports within the library so as to reconcile script and test importing (both assuming 'pretext' as a separate module), as well as publishing of the library. The logic behind the modules within the library follow a action-model-process separation in which _actions_ include the building blocks of the business model, _model_ includes the data structures, and _process_ allow for modular management of chunks of _actions_. Hence, _model_ should only be accessed by _actions_, and _actions_ should be only accessed by _process_.

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
|    -- model (data structures)
|    |
|    |
|    -- process (modular managers of actions)
|
-- tests   

## Run
python pretext.py --knowledge-files list_of_files_here
### Example: _python pretext.py --knowledge-files pretext.py pretext/actions/token.py_

## Test
Running all tests: _python -m unittest discover tests_

Running a specific test component: _python -m unittest test_module_qulaified_path_here_
### Example: _python -m unittest tests.test_text_actions_
### Example: _python -m unittest tests.test_text_actions.TestTokenActions.test_tokenize_by_words_3_
