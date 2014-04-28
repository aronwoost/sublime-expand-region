try:
  import expand_to_word
  import expand_to_word_with_dots
  import expand_to_symbols
  import expand_to_quotes
  import expand_to_semantic_unit
  import utils
except:
  from . import expand_to_word
  from . import expand_to_word_with_dots
  from . import expand_to_symbols
  from . import expand_to_quotes
  from . import expand_to_semantic_unit
  from . import utils

def expand(string, start, end):

  if utils.selection_contain_linebreaks(string, start, end) == False:

    line = utils.get_line(string, start, end)
    lineString = string[line["start"]:line["end"]]

    lineResult = expand_agains_line(lineString, start - line["start"], end - line["start"])

    if(lineResult):
      lineResult["start"] = lineResult["start"] + line["start"]
      lineResult["end"] = lineResult["end"] + line["start"]
      lineResult[string] = string[lineResult["start"]:lineResult["end"]];
      return lineResult

  expand_stack = ["semantic_unit"]

  result = expand_to_semantic_unit.expand_to_semantic_unit(string, start, end)
  if result:
    result["expand_stack"] = expand_stack
    return result

  expand_stack.append("symbols")

  result = expand_to_symbols.expand_to_symbols(string, start, end)
  if result:
    result["expand_stack"] = expand_stack
    return result

  print(None)

def expand_agains_line(string, start, end):
  expand_stack = []

  expand_stack.append("word")

  result = expand_to_word.expand_to_word(string, start, end)
  if result:
    result["expand_stack"] = expand_stack
    return result

  expand_stack.append("quotes")

  result = expand_to_quotes.expand_to_quotes(string, start, end)
  if result:
    result["expand_stack"] = expand_stack
    return result

  expand_stack.append("semantic_unit")

  result = expand_to_semantic_unit.expand_to_semantic_unit(string, start, end)
  if result:
    result["expand_stack"] = expand_stack
    return result

  expand_stack.append("symbols")

  result = expand_to_symbols.expand_to_symbols(string, start, end)
  if result:
    result["expand_stack"] = expand_stack
    return result

  expand_stack.append("line")

  # result = expand_to_line.expand_to_line(string, start, end)
  # if result:
  #   result["expand_stack"] = expand_stack
  #   return result

  # return None