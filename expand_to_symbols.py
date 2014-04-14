import re

try:
  import utils
except:
  from . import utils

def expand_to_symbols(string, startIndex, endIndex):
  openingSymbols = "([{";
  closingSymbols = ")]}";
  symbolsRe = re.compile(r'(['+re.escape(openingSymbols + closingSymbols)+'])')

  counterparts = {
    "(":")",
    "{":"}",
    "[":"]",
    ")":"(",
    "}":"{",
    "]":"["
  }

  symbolStack = []

  searchIndex = startIndex - 1;
  while True:
    if(searchIndex < 0):
      return None
    char = string[searchIndex:searchIndex+1]
    result = symbolsRe.match(char)
    if result:
      symbol = result.group()
      if(symbol in openingSymbols and len(symbolStack) == 0):
        newStartIndex = searchIndex + 1
        break
      else:
        if len(symbolStack) > 0 and symbolStack[len(symbolStack) - 1] == counterparts[symbol]:
          symbolStack.pop()
        else:
          symbolStack.append(symbol)
    searchIndex -= 1


  symbolPairRe = re.compile(r'(['+re.escape(symbol + counterparts[symbol])+'])')

  symbolStack = [symbol]

  searchIndex = endIndex;
  while True:
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
      break

    searchIndex += 1

  try:
    if(startIndex == newStartIndex and endIndex == newEndIndex):
      return utils.create_return_obj(newStartIndex - 1, newEndIndex + 1, string, "symbol")
    else:
      return utils.create_return_obj(newStartIndex, newEndIndex, string, "symbol")
  except NameError:
    return None