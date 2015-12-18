import re

try:
  import utils
except:
  from . import utils

def expand_to_xml_node(string, start, end):
  tag_properties = get_tag_properties(string[start:end])
  # if we are selecting a tag, then select the matching tag
  if tag_properties:
    tag_name = tag_properties["name"]
    if tag_properties["type"] == "closing":
      stringStartToTagStart = string[:start]
      openingTagPosition = find_tag(stringStartToTagStart, "backward", tag_name)
      if openingTagPosition:
        return utils.create_return_obj(openingTagPosition["start"], end, string, "complete_node")
    # if it's a opening tag, find opening tag and return positions
    elif tag_properties["type"] == "opening":
      stringNodeEndToStringEnd = string[end:]
      closingTagPosition = find_tag(stringNodeEndToStringEnd, "forward", tag_name)
      if closingTagPosition:
        return utils.create_return_obj(start, end + closingTagPosition["end"], string, "complete_node")
    # else it's self closing and there is no matching tag

  # check if current selection is within a tag, if it is expand to the tag
  # first expand to inside the tag and then to the whole tag
  is_within_tag_result = is_within_tag(string, start, end)
  if is_within_tag_result:
    inner_start = is_within_tag_result["start"] + 1
    inner_end = is_within_tag_result["end"] - 1
    if start == inner_start and end == inner_end:
      return utils.create_return_obj(is_within_tag_result["start"], is_within_tag_result["end"], string, "complete_node")
    else:
      return utils.create_return_obj(inner_start, inner_end, string, "inner_node")
  # expand selection to the "parent" node of the current selection
  stringStartToSelectionStart = string[:start]
  parent_opening_tag = find_tag(stringStartToSelectionStart, "backward")
  if(parent_opening_tag):
    # find closing tag
    stringNodeEndToStringEnd = string[parent_opening_tag["end"]:]
    closingTagPosition = find_tag(stringNodeEndToStringEnd, "forward", parent_opening_tag["name"])
    if closingTagPosition:
      # set positions to content of node, w/o the node tags
      newStart = parent_opening_tag["end"]
      newEnd = parent_opening_tag["end"] + closingTagPosition["start"]

      # if this is the current selection, set positions to content of node including start and end tags
      if(newStart == start and newEnd == end):
        newStart = parent_opening_tag["start"]
        newEnd = parent_opening_tag["end"] + closingTagPosition["end"]

      return utils.create_return_obj(newStart, newEnd, string, "parent_node_content")

def is_within_tag(string, startIndex, endIndex):
  openingRe = re.compile("<");
  closingRe = re.compile(">");

  # look back
  searchIndex = startIndex - 1;
  while True:
    # begin of string is reached, let's return here
    if searchIndex < 0:
      return False
    char = string[searchIndex:searchIndex+1]
    # tag start found!
    if openingRe.match(char):
      newStartIndex = searchIndex
      break;
    # closing tag found, let's return here
    if closingRe.match(char):
      return False
    searchIndex -= 1

  # look forward
  searchIndex = endIndex;
  while True:
    # end of string is reached, let's return here
    if searchIndex > len(string) - 1:
      return False
    char = string[searchIndex:searchIndex+1]
    # tag start found!
    if closingRe.match(char):
      return {"start": newStartIndex, "end": searchIndex + 1}
    # closing tag found, let's return here
    if openingRe.match(char):
      return False
    searchIndex += 1

# returns tag name and if tag has a closing slash
def get_tag_properties(string):
  regex = re.compile(
    r"<\s*"
    r"(?P<closing>\/?)\s*"
    r"(?P<name>[^\s\/]*)\s*"
    r"(?:.*?)"
    r"(?P<self_closing>\/?)\s*"
    r">"
  )
  result = regex.match(string)
  if not result:
    return None

  tag_name = result.group("name")

  void_elements = ["area", "base", "br", "col", "embed", "hr", "img", "input", "keygen", "link", "meta", "param", "source", "track", "wbr"]

  if result.group("closing"):
    tag_type = "closing"
  elif result.group("self_closing"):
    tag_type = "self_closing"
  elif(tag_name in void_elements):
    tag_type = "self_closing"
  else:
    tag_type = "opening"

  return {"name": tag_name, "type": tag_type}

def find_tag(string, direction, tag_name=""):
  # search for opening and closing tag with a tag_name. If tag_name = "", search
  # for all tags.
  regexString = "<\s*" + tag_name + ".*?>|<\/\s*" + tag_name + "\s*>"
  regex = re.compile(regexString)

  # direction == "forward" implies that we are looking for closing tags (and
  # vice versa
  target_tag_type = (direction == "forward" and "closing" or "opening")
  # set counterpart
  target_tag_type_counterpart = (direction == "forward" and "opening" or "closing")

  # found tags will be added/removed from the stack to eliminate complete nodes
  # (opening tag + closing tag).
  symbolStack = []

  result = list(regex.finditer(string))

  # since regex can't run backwards, we reverse the result
  if(direction == "backward"):
    result.reverse()

  for m in result:
    tag_string = m.group()
    # ignore comments
    if tag_string.startswith("<!--"):
      continue
    tag_type = get_tag_properties(tag_string)["type"]
    if(tag_type == target_tag_type):
      if(len(symbolStack) == 0):
        return {"start": m.start(), "end": m.end(), "name": get_tag_properties(tag_string)["name"]}
      symbolStack.pop()
    elif(tag_type == target_tag_type_counterpart):
      symbolStack.append(tag_type)
