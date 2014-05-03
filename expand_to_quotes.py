import re

try:
  import utils
except:
  from . import utils

def expand_to_quotes(string, startIndex, endIndex):
  quotesRe = re.compile(r'([\'"])(?:\1|.*?[^\\]\1)')

  # iterate over all found quotes pairs
  for match in re.finditer(quotesRe, string):
    start = match.start(0)
    end = match.end(0)

    if end < startIndex:
      continue

    if(startIndex == start and endIndex == end):
      return None

    # current selection is within the found quote pairs
    if(startIndex > start and endIndex < end):
      if(startIndex == start + 1 and endIndex == end - 1):
        if(startIndex == start and endIndex == end):
          return None
        else:
          return utils.create_return_obj(start, end, string, "quotes")
      else:
        return utils.create_return_obj(start + 1, end - 1, string, "quotes")