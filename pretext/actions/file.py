def read_text_file(fileName):
  with open(fileName, 'r') as f:
    data = f.read()
    return data 
