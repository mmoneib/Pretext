def tokenize(text):
  return __tokenize_by_char(text)

def __tokenize_by_char(text):
  tokens=[]
  for c in text:
    tokens+=c
  return tokens
