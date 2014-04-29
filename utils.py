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

def get_line(string, startIndex, endIndex):
  linebreakRe = re.compile(r'\n')

  searchIndex = startIndex - 1;
  while True:
    if searchIndex < 0:
      newStartIndex = searchIndex + 1
      break
    char = string[searchIndex:searchIndex+1]
    if linebreakRe.match(char):
      newStartIndex = searchIndex + 1
      break
    else:
      searchIndex -= 1

  searchIndex = endIndex;
  while True:
    if searchIndex > len(string) - 1:
      newEndIndex = searchIndex
      break
    char = string[searchIndex:searchIndex+1]
    if linebreakRe.match(char):
      newEndIndex = searchIndex
      break
    else:
      searchIndex += 1

  return {"start": newStartIndex, "end": newEndIndex}

def trim(string):
  # TODO can s.strip() be used for that?
  trim = re.compile(r'^[ \t\n]*(.*?)[ \t\n]*$', re.DOTALL)
  r = trim.search(string)

  if r:
    return {"start": r.start(1), "end": r.end(1)}
  else:
    return None