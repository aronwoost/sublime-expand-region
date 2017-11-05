import re

try:
  # Block it from trying to import something which should not be on the python sys.path
  # https://github.com/hktonylee/SublimeNumberKing/issues/4
  import expand_region_handler
  import utils
except:
  from . import utils

def expand_to_quotes(string, selection_start, selection_end):
  quotes_regex = re.compile("(['\"])(?:\\\.|.)*?\\1")

  # iterate over all found quotes pairs
  for match in quotes_regex.finditer(string):
    quotes_start = match.start()
    quotes_end = match.end()

    # quotes pair end is before selection, stop here and continue loop
    if quotes_end < selection_start:
      continue

    # quotes pair start is after selection, return, no need to continue loop
    if quotes_start > selection_end:
      return None

    # quotes are already selection_end
    if(selection_start == quotes_start and selection_end == quotes_end):
      return None

    # the string w/o the quotes, "quotes content"
    quotes_content_start = quotes_start + 1
    quotes_content_end = quotes_end - 1

    # "quotes content" is selected, return with quotes
    if(selection_start == quotes_content_start and selection_end == quotes_content_end):
      return utils.create_return_obj(quotes_start, quotes_end, string, "quotes")

    # selection is within the found quote pairs, return "quotes content"
    if(selection_start > quotes_start and selection_end < quotes_end):
      return utils.create_return_obj(quotes_content_start, quotes_content_end, string, "quotes")
