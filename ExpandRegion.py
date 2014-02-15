import sublime, sublime_plugin, expand_region_handler

class ExpandRegionCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    region = self.view.sel()[0]
    string = self.view.substr(sublime.Region(0, self.view.size()))
    start = region.begin()
    end = region.end()

    result = expand_region_handler.expand(string, start, end)
    if result:
      self.view.sel().add(sublime.Region(result["start"], result["end"]))