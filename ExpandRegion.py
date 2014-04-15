import sublime, sublime_plugin, os

try:
  import expand_region_handler
except:
  from . import expand_region_handler

class ExpandRegionCommand(sublime_plugin.TextCommand):
  def run(self, edit, debug=False):
    
    name, extension = os.path.splitext(self.view.file_name())

    region = self.view.sel()[0]
    string = self.view.substr(sublime.Region(0, self.view.size()))
    start = region.begin()
    end = region.end()

    result = expand_region_handler.expand(string, start, end, extension[1:])
    if result:
      self.view.sel().add(sublime.Region(result["start"], result["end"]))
      if debug:
        print("startIndex: {0}, endIndex: {1}, type: {2}".format(result["start"], result["end"], result["type"]))