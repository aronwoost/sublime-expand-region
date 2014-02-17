import re

def expand(string, start, end):
  result = expand_to_word(string, start, end)
  if result is None:
    result = expand_to_quotes(string, start, end)
    if result is None:
      result = expand_to_symbols(string, start, end)
      if result is None:
        print None
      else:
        return result
    else:
      return result
  else:
    return result

def expand_to_word(string, startIndex, endIndex):
  wordRe = re.compile("^[a-zA-Z0-9_]*$");
  wordRe2 = re.compile("[a-zA-Z0-9_]*$");

  if(startIndex != endIndex):
    selection = string[startIndex:endIndex]
    if wordRe2.match(selection) is None:
      return None

  search = True;
  searchIndex = startIndex - 1;
  while search:
    if searchIndex < 0:
      search = False
      break
    char = string[searchIndex:searchIndex+1]
    if wordRe.match(char) is None:
      newStartIndex = searchIndex + 1
      search = False
    else:
      searchIndex -= 1

  search = True;
  searchIndex = endIndex;
  while search:
    if searchIndex > len(string) - 1:
      search = False
      break
    char = string[searchIndex:searchIndex+1]
    if wordRe.match(char) is None:
      newEndIndex = searchIndex
      search = False
    else:
      searchIndex += 1

  try:
    if startIndex == newStartIndex and endIndex == newEndIndex:
      return None
    else:
      return create_return_obj(newStartIndex, newEndIndex, string, "word")
  except NameError:
    return None

def expand_to_quotes(string, startIndex, endIndex):
  quotesRe = re.compile(r'([\'"])(?:\1|.*?[^\\]\1)')

  for match in re.finditer(quotesRe, string):
    start = match.start(0)
    end = match.end(0)

    if end < startIndex:
      continue

    if(startIndex == start and endIndex == end):
      return None

    if(startIndex >= start and endIndex <= end):
      if(startIndex == start + 1 and endIndex == end - 1):
        if(startIndex == start and endIndex == end):
          return None
        else:
          return create_return_obj(start, end, string, "quotes")
      else:
        return create_return_obj(start + 1, end - 1, string, "quotes")

def expand_to_symbols(string, startIndex, endIndex):
  openingSymbols = "([{";
  closingSymbols = ")]}";
  quotesRe = re.compile(r'(['+re.escape(openingSymbols + closingSymbols)+'])')

  counterparts = {
    "(":")",
    "{":"}",
    "[":"]",
    ")":"(",
    "}":"{",
    "]":"["
  }

  symbolStack = []

  search = True;
  searchIndex = startIndex - 1;
  while search:
    if(searchIndex < 0):
      return None
    char = string[searchIndex:searchIndex+1]
    result = quotesRe.match(char)
    if result:
      symbol = result.group()
      if(symbol in openingSymbols and len(symbolStack) == 0):
        symbolToFind = symbol
        newStartIndex = searchIndex + 1
        search = False
      else:
        if len(symbolStack) > 0 and symbolStack[len(symbolStack) - 1] == counterparts[symbol]:
          symbolStack.pop()
        else:
          symbolStack.append(symbol)
      searchIndex -= 1
    else:
      searchIndex -= 1


  symbolPairRe = re.compile(r'(['+re.escape(symbolToFind)+re.escape(counterparts[symbolToFind])+'])')

  symbolStack = [symbolToFind]

  search = True;
  searchIndex = endIndex;
  while search:
    char = string[searchIndex:searchIndex+1]
    result = symbolPairRe.match(char)
    if result:
      symbol = result.group()

      if symbolStack[len(symbolStack) - 1] == counterparts[symbol]:
        symbolStack.pop()
      else:
        symbolStack.append(symbol)

      if len(symbolStack) == 0:
        newEndIndex = searchIndex;
        break

    if searchIndex == len(string):
      search = False

    searchIndex += 1

  try:
    if(startIndex == newStartIndex and endIndex == newEndIndex):
      return create_return_obj(newStartIndex - 1, newEndIndex + 1, string, "symbol")
    else:
      return create_return_obj(newStartIndex, newEndIndex, string, "symbol")
  except NameError:
    return None

def create_return_obj(start, end, string, type):
  return {"start": start, "end": end, "string": string[start:end], "type": type}