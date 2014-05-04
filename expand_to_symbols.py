import re

try:
  import utils
except:
  from . import utils

def expand_to_symbols(string, selection_start, selection_end):
  opening_symbols = "([{";
  closing_symbols = ")]}";
  symbols_regex = re.compile("[" + re.escape(opening_symbols + closing_symbols)+"]")

  counterparts = {
    "(":")",
    "{":"}",
    "[":"]",
    ")":"(",
    "}":"{",
    "]":"["
  }

  symbol_stack = []

  search_index = selection_start - 1;
  while True:
    # begin of string reached
    if(search_index < 0):
      return None

    character = string[search_index:search_index + 1]
    result = symbols_regex.match(character)

    if result:
      symbol = result.group()

      # symbol is opening symbol and stack is empty, we found the symbol we want to expand to
      if(symbol in opening_symbols and len(symbol_stack) == 0):
        symbols_start = search_index + 1
        break

      if len(symbol_stack) > 0 and symbol_stack[len(symbol_stack) - 1] == counterparts[symbol]:
        # last symbol in the stack is the counterpart of the found one
        symbol_stack.pop()
      else:
        symbol_stack.append(symbol)

    search_index -= 1

  symbol_pair_regex = re.compile("[" + re.escape(symbol + counterparts[symbol]) + "]")

  symbol_stack = [symbol]

  search_index = selection_end;
  while True:
    character = string[search_index:search_index + 1]
    result = symbol_pair_regex.match(character)

    if result:
      symbol = result.group()

      if symbol_stack[len(symbol_stack) - 1] == counterparts[symbol]:
        # counterpart of found symbol is the last one in stack, remove it
        symbol_stack.pop()
      else:
        symbol_stack.append(symbol)

      if len(symbol_stack) == 0:
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
