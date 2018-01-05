def dataSetLetters(string):
  """"Help function to find dataset letter(s) (ABCDE) at the beginning of a string"""
  letters = ""
  dataSetLetters = [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'H', 'I', 'J', 'K' ]
  if len(string)>0:
    for character in string:
      print "%s <-> %s"%(character,dataSetLetters)
      if len(dataSetLetters)==0: break
      
      for i, letter in enumerate(dataSetLetters):
        if character == letter:
          letters += letter
          dataSetLetters = dataSetLetters[i+1:]
          break
      else: break
  return letters


print dataSetLetters("ABloldege")
print dataSetLetters("BCdegdee")
print dataSetLetters("Fpoplo")
print dataSetLetters("GJsdhej")
print dataSetLetters("IKsdfdhej")
print dataSetLetters("egwgb")
print dataSetLetters("")