def openTextFileAsReadOnly(fileName):
  with open(fileName, 'r') as f:
    data = f.read()
    return data 
