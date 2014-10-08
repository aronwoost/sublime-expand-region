import re

try:
  import utils
except:
  from . import utils

def expand_to_symbols(string, selection_start, selection_end):
  opening_symbols = "([{";
  closing_symbols = ")]}";
  symbols_regex = re.compile("[" + re.escape(opening_symbols + closing_symbols)+"]")

  quotes_regex = re.compile("(['\"])(?:\\1|.*?\\1)")
  quotes_blacklist = {}

  # get all quoted strings and create dict with key of index = True
  # Example: f+"oob"+bar
  # quotes_blacklist = {
  #   2: true, 3: true, 4: true, 5: true, 6: true
  # }
  for match in quotes_regex.finditer(string):
    quotes_start = match.start()
    quotes_end = match.end()
    i = 0;
    while True:
      quotes_blacklist[quotes_start + i] = True
      i += 1
      if (quotes_start + i == quotes_end):
        break;

  counterparts = {
    "(":")",
    "{":"}",
    "[":"]",
    ")":"(",
    "}":"{",
    "]":"["
  }

  # find symbols in selection that are "not closed"
  selection_string = string[selection_start:selection_end]
  selection_quotes = symbols_regex.findall(selection_string)

  backward_symbols_stack = []
  forward_symbols_stack = []

  if(len(selection_quotes) != 0):
    inspect_index = 0
    # remove symbols that have a counterpart, i.e. that are "closed"
    while True:
      item = selection_quotes[inspect_index]
      if(counterparts[item] in selection_quotes):
        del selection_quotes[selection_quotes.index(item)]
        del selection_quotes[selection_quotes.index(counterparts[item])]
      else:
        inspect_index = inspect_index + 1
      if(inspect_index >= len(selection_quotes)):
        break;

    # put the remaining "open" symbols in the stack lists depending if they are
    # opening or closing symbols
    for item in selection_quotes:
      if(item in opening_symbols):
        forward_symbols_stack.append(item)
      elif(item in closing_symbols):
        backward_symbols_stack.append(item)

  search_index = selection_start - 1;

  # look back from begin of selection
  while True:
    # begin of string reached
    if(search_index < 0):
      return None

    # skip if current index is within a quote
    if (quotes_blacklist.get(search_index, False) == True):
      search_index -= 1
      continue;
    character = string[search_index:search_index + 1]
    result = symbols_regex.match(character)

    if result:
      symbol = result.group()

      # symbol is opening symbol and stack is empty, we found the symbol we want to expand to
      if(symbol in opening_symbols and len(backward_symbols_stack) == 0):
        symbols_start = search_index + 1
        break

      if len(backward_symbols_stack) > 0 and backward_symbols_stack[len(backward_symbols_stack) - 1] == counterparts[symbol]:
        # last symbol in the stack is the counterpart of the found one
        backward_symbols_stack.pop()
      else:
        backward_symbols_stack.append(symbol)

    search_index -= 1

  symbol_pair_regex = re.compile("[" + re.escape(symbol + counterparts[symbol]) + "]")

  forward_symbols_stack.append(symbol)

  search_index = selection_end;

  # look forward from end of selection
  while True:
    # skip if current index is within a quote
    if (quotes_blacklist.get(search_index, False) == True):
      search_index += 1
      continue;
    character = string[search_index:search_index + 1]
    result = symbol_pair_regex.match(character)

    if result:
      symbol = result.group()

      if forward_symbols_stack[len(forward_symbols_stack) - 1] == counterparts[symbol]:
        # counterpart of found symbol is the last one in stack, remove it
        forward_symbols_stack.pop()
      else:
        forward_symbols_stack.append(symbol)

      if len(forward_symbols_stack) == 0:
        symbols_end = search_index;
        break

    # end of string reached
    if search_index == len(string):
      return

    search_index += 1

  if(selection_start == symbols_start and selection_end == symbols_end):
    return utils.create_return_obj(symbols_start - 1, symbols_end + 1, string, "symbol")
  else:
    return utils.create_return_obj(symbols_start, symbols_end, string, "symbol")
