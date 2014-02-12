import sublime, sublime_plugin, re

class ExpandRegionCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    region = self.view.sel()[0]
    string = self.view.substr(sublime.Region(0, self.view.size()))
    start = region.begin()
    end = region.end()

    if self.expand_to_word(string, start, end) is None:
      print "none"
  
  def expand_to_word(self, string, startIndex, endIndex):
    wordRe = re.compile("^[a-zA-Z0-9_]*$");

    search = True;
    searchIndex = startIndex;
    while search:
      char = string[searchIndex:searchIndex+1]
      if wordRe.match(char) is None:
        newStartIndex = searchIndex + 1
        search = False
      else:
        searchIndex -= 1

    search = True;
    searchIndex = endIndex;
    while search:
      char = string[searchIndex:searchIndex+1]
      if wordRe.match(char) is None:
        newEndIndex = searchIndex
        search = False
      else:
        searchIndex += 1


    if startIndex == newStartIndex and endIndex == newEndIndex:
      return None
    else:
      self.view.sel().add(sublime.Region(newStartIndex, newEndIndex))
      return True