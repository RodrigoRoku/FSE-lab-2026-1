
index = 0

def formNextPrintableWord(nombre):
  global index
  i = index
  printable = ""
  for char in range(16):
    if(i >= len(nombre)):
      i = 0
    printable += nombre[i]
    i += 1
    
  index = index + 1 
  if(index >= len(nombre)):
    index = 0
  
  return printable