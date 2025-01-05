import re

commonWords = {" the ", " of ", " to ", " on ", " at ", " for ", " by ", " a ", " an ", " in ", " and ", " is ", " was ", " are ", " he ", " she ", " it ", " as ", " if ", " that ", " his ", " her ", " I ", " him "} # Padded to avoid replacing parts of other words.

def remove_common_words(text, commonWordReplacement): # Replaces the common word with a common prefix for the next.
  if commonWordReplacement.isspace() or commonWordReplacement == "":
    if commonWordReplacement == "":
      commonWordReplacement = " " # Needed to avoid conjoining words.
    for cw in commonWords:
      text = text.replace(cw, commonWordReplacement)
  else:
    paddedCommonWordReplacement = " {} ".format(commonWordReplacement)
    for cw in commonWords:
      text = text.replace(cw, paddedCommonWordReplacement)
    unpaddedBeforeCommonWordReplacement = paddedCommonWordReplacement[1:]
    text = text.replace(unpaddedBeforeCommonWordReplacement, commonWordReplacement) # Prefixing next words.
  return text

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

def tokenize_by_chars_simplified(text, numOfCharsInToken):
  tokensList=[]
  windowStart=0
  windowEnd=numOfCharsInToken
  textSize=len(text)
  while windowStart < textSize:
    token=text[windowStart:windowEnd] 
    tokensList.append(token)
    windowStart=windowStart+1
    windowEnd=windowEnd+1
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

def count_words(text): # Counting through negative (non-word) consecutive characters. Effectively counts spaces between words.
  return len(re.findall(r'[\ |\t]+',text)) + 1 # TODO Look for a more optimized way that counts by searching only without creating a list.
