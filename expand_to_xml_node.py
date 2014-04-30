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
    # if it's a closing tag, find opening tag and return prositions
    if(getTagNameResult["has_closing_slash"]):
      stringStartToTagEnd = string[0:is_within_tag_result["end"]]
      openingTagPosition = find_opening_tag(stringStartToTagEnd, tagName)
      return utils.create_return_obj(openingTagPosition["start"], is_within_tag_result["end"], string, "complete_node")
    # if it's a opening tag, find opening tag and return prositions
    else:
      stringNodeStartToStringEnd = string[is_within_tag_result["start"]:]
      closingTagPosition = find_closing_tag(stringNodeStartToStringEnd, tagName)
      return utils.create_return_obj(is_within_tag_result["start"], is_within_tag_result["start"] + closingTagPosition["end"], string, "complete_node")

  # expand selection to the "parent" node of the current selection
  stringStartToSelectionStart = string[0:start]
  parent_opening_tag = find_parent_open_tag(stringStartToSelectionStart)
  if(parent_opening_tag):
    # find closing tag
    stringNodeStartToStringEnd = string[parent_opening_tag["start"]:]
    closingTagPosition = find_closing_tag(stringNodeStartToStringEnd, parent_opening_tag["name"])

    # set positions to content of node, w/o the node tags
    newStart = parent_opening_tag["end"]
    newEnd = parent_opening_tag["start"] + closingTagPosition["start"]

    # if this is the current selection, set positions to content of node including start and end tags
    if(newStart == start and newEnd == end):
      newStart = parent_opening_tag["start"]
      newEnd = parent_opening_tag["start"] + closingTagPosition["end"]

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
  regex = re.compile("<[\s]*(\/*)(.*?)[>|\s]")

  result = regex.match(string)
  return {"name": result.group(2), "has_closing_slash": result.group(1) == "/"}

def find_closing_tag(string, tag_name):
  regexString = "<\s*" + tag_name + "(?:.*?)>|<\/\s*" + tag_name + "\s*>"
  regex = re.compile(regexString)

  opening = "<>"
  closing = "</>"
  symbolStack = []

  result = regex.finditer(string)
  for m in result:
    tag = sanitize_tag_chars(m.group())
    if(tag == opening):
      symbolStack.append(tag)
    elif(tag == closing):
      symbolStack.pop()

    if(len(symbolStack) == 0):
      return {"start": m.start(), "end": m.end()}

def find_opening_tag(string, tag_name):
  regexString = "<\s*" + tag_name + "(?:.*?)>|<\/\s*" + tag_name + "\s*>"
  regex = re.compile(regexString)

  opening = "<>"
  closing = "</>"
  symbolStack = []

  result = list(regex.finditer(string))
  result.reverse()

  for m in result:
    tag = sanitize_tag_chars(m.group())
    if(tag == closing):
      symbolStack.append(tag)
    elif(tag == opening):
      symbolStack.pop()

    if(len(symbolStack) == 0):
      return {"start": m.start(), "end": m.end()}

def sanitize_tag_chars(string):
  regex = re.compile("<|>|\/")
  result = regex.findall(string)
  return "".join(result)

def find_parent_open_tag(string):
  regexString = "<(?:.*?)>|<\/(?:.*?)>"
  regex = re.compile(regexString)

  opening = "<>"
  closing = "</>"
  symbolStack = []

  result = list(regex.finditer(string))
  result.reverse()

  for m in result:
    tag = sanitize_tag_chars(m.group())
    if(tag == opening):
      if(len(symbolStack) == 0):
        return {"start": m.start(), "end": m.end(), "name": get_tag_properties(m.group())["name"]}
      symbolStack.pop()
    elif(tag == closing):
      symbolStack.append(tag)