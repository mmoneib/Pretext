def tokenize(text):
  return __tokenize_by_char(text)

def __tokenize_by_char(text):
  tokens=[]
  for c in text:
    tokens+=c
  return tokens

def __tokenize_by_word(text):
  tokens=[]
  word=""
  for c in text:
    tokens+=c
    if c == " " or c == "\n" or c == "\r":
      tokens+=word
      word=""
  return tokens
