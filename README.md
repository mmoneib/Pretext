# Pretext
A text predictor based on statistical inference.

## Run
python pretext/pretext.py --knowledge-files list_of_files_here
### Example: _python pretext/pretext.py --knowledge-files pretext/pretext.py pretext/actions/token.py_

## Test
python -m unittest test_module_qulaified_path_here
### Example: _python -m unittest tests.test_text_actions_
### Example: _python -m unittest tests.test_text_actions.TestTokenActions.test_tokenize_by_words_3_
