import re

def selection_contain_linebreaks(string, startIndex, endIndex):
  linebreakRe = re.compile("(\n)")
  part = string[startIndex:endIndex]

  result = linebreakRe.search(part)
  if result:
    return True
  else:
    return False

def create_return_obj(start, end, string, type):
  return {"start": start, "end": end, "string": string[start:end], "type": type}