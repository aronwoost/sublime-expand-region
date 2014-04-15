try:
  import expand_to_word
except:
  from . import expand_to_word

def expand(string, start, end):
  expand_stack = []

  expand_stack.append("word")

  result = expand_to_word.expand_to_word(string, start, end)
  if result:
    result["expand_stack"] = expand_stack
    return result


def expand_agains_line(string, start, end):
  print("line")