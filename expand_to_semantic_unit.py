import re

try:
  import utils
except:
  from . import utils

# This function definitely sucks and needs a serious rework. Finding semantic
# units is not that easy. Maybe a parser is needed?
def expand_to_semantic_unit(string, startIndex, endIndex):
  symbols = "([{)]}"
  breakSymbols = ",;=&|\n"
  lookBackBreakSymbols = breakSymbols + "([{"
  lookForwardBreakSymbols = breakSymbols + ")]}"
  symbolsRe = re.compile(r'(['+re.escape(symbols)+re.escape(breakSymbols)+'])')

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
      newStartIndex = searchIndex + 1
      break
    char = string[searchIndex:searchIndex+1]
    result = symbolsRe.match(char)
    if result:
      symbol = result.group()

      if(symbol in lookBackBreakSymbols and len(symbolStack) == 0):
        newStartIndex = searchIndex + 1
        break

      if symbol in symbols:
        if len(symbolStack) > 0 and symbolStack[len(symbolStack) - 1] == counterparts[symbol]:
          symbolStack.pop()
        else:
          symbolStack.append(symbol)

    # print(char, symbolStack)
    searchIndex -= 1

  searchIndex = endIndex;
  while True:
    char = string[searchIndex:searchIndex+1]
    result = symbolsRe.match(char)
    if result:
      symbol = result.group()

      if len(symbolStack) == 0 and symbol in lookForwardBreakSymbols:
        newEndIndex = searchIndex;
        break

      if symbol in symbols:
        if len(symbolStack) > 0 and symbolStack[len(symbolStack) - 1] == counterparts[symbol]:
          symbolStack.pop()
        else:
          symbolStack.append(symbol)

    if searchIndex >= len(string) - 1:
      return None

    # print(char, symbolStack, searchIndex)
    searchIndex += 1

  s = string[newStartIndex:newEndIndex]
  trimResult = utils.trim(s)
  if trimResult:
    newStartIndex = newStartIndex + trimResult["start"];
    newEndIndex = newEndIndex - (len(s) - trimResult["end"]);

  try:
    if newStartIndex == startIndex and newEndIndex == endIndex:
      return None

    if newStartIndex > startIndex or newEndIndex < endIndex:
      return None

    return utils.create_return_obj(newStartIndex, newEndIndex, string, "semantic_unit")
  except NameError:
    return None