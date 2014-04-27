import re

try:
  import expand_to_regex_set
except:
  from . import expand_to_regex_set

def expand_to_word_with_dots(string, startIndex, endIndex):
  regex = re.compile("[a-zA-Z0-9_$.]");

  return expand_to_regex_set._expand_to_regex_rule(string, startIndex, endIndex, regex, "word_with_dots")