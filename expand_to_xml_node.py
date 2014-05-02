import re

try:
  import utils
except:
  from . import utils

def expand_to_xml_node(string, start, end):

  # check if current selection is with a tag
  is_within_tag_result = is_within_tag(string, start, end)
  if(is_within_tag_result):
    # save string of tag
    tagString = string[is_within_tag_result["start"]:is_within_tag_result["end"]]
    # get tag name and if it's a opening or closing tag
    getTagNameResult = get_tag_properties(tagString)
    tagName = getTagNameResult["name"]
    # if it's a closing tag, find opening tag and return positions
    if(getTagNameResult["type"] == "closing"):
      stringStartToTagStart = string[0:is_within_tag_result["start"]]
      openingTagPosition = find_tag(stringStartToTagStart, "backward", tagName)
      return utils.create_return_obj(openingTagPosition["start"], is_within_tag_result["end"], string, "complete_node")
    # it's self closing, just use it, no need to look further
    elif(getTagNameResult["type"] == "self_closing"):
      return utils.create_return_obj(is_within_tag_result["start"], is_within_tag_result["end"], string, "complete_node")
    # if it's a opening tag, find opening tag and return positions
    else:
      stringNodeEndToStringEnd = string[is_within_tag_result["end"]:]
      closingTagPosition = find_tag(stringNodeEndToStringEnd, "forward", tagName)
      return utils.create_return_obj(is_within_tag_result["start"], is_within_tag_result["end"] + closingTagPosition["end"], string, "complete_node")

  # expand selection to the "parent" node of the current selection
  stringStartToSelectionStart = string[0:end]
  parent_opening_tag = find_tag(stringStartToSelectionStart, "backward")
  if(parent_opening_tag):
    # find closing tag
    stringNodeEndToStringEnd = string[parent_opening_tag["end"]:]
    closingTagPosition = find_tag(stringNodeEndToStringEnd, "forward", parent_opening_tag["name"])

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
  regex = re.compile("<\s*(\/*)\s*(\S*)(?:.*?)(\/*)\s*>")
  result = regex.match(string)

  tag_name = result.group(2)

  void_elements = ["area", "base", "br", "col", "embed", "hr", "img", "input", "keygen", "link", "meta", "param", "source", "track", "wbr"]

  if(result.group(1) == "/"):
    tag_type = "closing"
  elif(result.group(3) == "/"):
    tag_type = "self_closing"
  elif(tag_name in void_elements):
    tag_type = "self_closing"
  else:
    tag_type = "opening"

  return {"name": result.group(2), "type": tag_type}

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
    tag_type = get_tag_properties(m.group())["type"]
    if(tag_type == target_tag_type):
      if(len(symbolStack) == 0):
        return {"start": m.start(), "end": m.end(), "name": get_tag_properties(m.group())["name"]}
      symbolStack.pop()
    elif(tag_type == target_tag_type_counterpart):
      symbolStack.append(tag_type)