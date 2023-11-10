def tokenize_by_char(text):
  tokens=[]
  for c in text:
    tokens+=c
  return tokens

def tokenize_by_word(text):
  tokens=[]
  word=""
  for c in text:
    if c == ' ' or c == '\n':
      if word != "":
        tokens.append(word) # Must use append; otherwise, it would be a list of chars.
      word=""
    else:
      word+=c
  return tokens
