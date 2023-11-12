def tokenize_by_char(text):
  tokens=[]
  for c in text:
    tokens+=c
  return tokens

def tokenize_by_chars(text, numOfChars): # Another function as one char doesn't need a buffer.
  tokens=[]
  buff=""
  count=0
  for c in text:
    buff+=c
    if count == numOfChars-1:
      tokens.append(buff)
      buff=""
      count=8
    count=count+1
  return tokens

def tokenize_by_word(text):
  tokens=[]
  word=""
  for c in text:
    if c == ' ' or c == '\n':
      if word != "":
        tokens.append(word) # Must use append; otherwise, it would be a list of chars. Adding c for organic prediction of spaces and conclusions.
      word=""
    else:
      word+=c
  return tokens

def tokenize_by_words(text, numOfWords): # Another function as one char doesn't need a buffer.
  tokens=[]
  word=""
  buff=""
  count=0
  for c in text:
    if c == ' ' or c == '\n': #TODO Allow space and new line before a word but not after.
      if word.endswith(' ') == False and word.endswith('\n') == False: # That it is not a string of empty spaces.
        buff+=word # Can include empty spaces prior to the work.
        if count == numOfWords-1:
          tokens.append(buff)
          buff=""
          word=""
          count=0
        else:
          word+=c
        count=count+1
      #else:
        #word+=c # Adding empty space to empty spaces.
    else:
      word+=c
  return tokens
