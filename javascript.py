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
  selection_is_in_string = expand_to_quotes.expand_to_quotes(string, start, end)

  if selection_is_in_string:
    string_result = expand_agains_string(selection_is_in_string["string"], start - selection_is_in_string["start"], end - selection_is_in_string["start"])

    if string_result:
      string_result["start"] = string_result["start"] + selection_is_in_string["start"]
      string_result["end"] = string_result["end"] + selection_is_in_string["start"]
      string_result[string] = string[string_result["start"]:string_result["end"]];
      return string_result

  if utils.selection_contain_linebreaks(string, start, end) == False:

    line = utils.get_line(string, start, end)
    line_string = string[line["start"]:line["end"]]

    line_result = expand_agains_line(line_string, start - line["start"], end - line["start"])

    if line_result:
      line_result["start"] = line_result["start"] + line["start"]
      line_result["end"] = line_result["end"] + line["start"]
      line_result[string] = string[line_result["start"]:line_result["end"]];
      return line_result

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

  # expand_stack.append("line")

  # result = expand_to_line.expand_to_line(string, start, end)
  # if result:
  #   result["expand_stack"] = expand_stack
  #   return result

  # return None

def expand_agains_string(string, start, end):
  expand_stack = []

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
