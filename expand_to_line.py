import re

try:
  import utils
except:
  from . import utils

def expand_to_line(string, startIndex, endIndex):
  linebreakRe = re.compile(r'\n')

  spacesAndTabsRe = re.compile(r'([ \t]+)')

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

  s = string[newStartIndex:newEndIndex]
  r = spacesAndTabsRe.match(s)
  if r and r.end() <= startIndex:
    newStartIndex = newStartIndex + r.end();

  try:
    if startIndex == newStartIndex and endIndex == newEndIndex:
      return None
    else:
      return utils.create_return_obj(newStartIndex, newEndIndex, string, "line")
  except NameError:
    return None