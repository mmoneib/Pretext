def tokenize_by_chars(text, numOfCharsInToken):
  tokensList=[]
  if numOfCharsInToken==1: # Would have worked with 2nd condition alone, but this is for performance.
    for c in text:
      tokensList+=c
    return tokensList
  else:
    token=""
    for c in text:
      token+=c
      if len(token)==numOfCharsInToken:
        tokensList.append(token)
        token=""
    if token!="": # For the last token < numOfCharsInToken.
      tokensList.append(token)
    return tokensList

def tokenize_by_words(text, numOfWords):
  tokensList=[]
  token=""
  isEmpty=True
  wordsCount=0
  for c in text:
    if (c==' ' or c=='\n') and isEmpty==False:
      wordsCount=wordsCount+1
      if wordsCount==numOfWords:
        tokensList.append(token) # Must use append; otherwise, it would be a list of chars.
        token=""
        wordsCount=0
    if c==' ' or c=='\n':
      isEmpty=True
    else:
      isEmpty=False
    token+=c # Spaces and new-lines after last word included.
  if token!="":
    tokensList.append(token)
  return tokensList
