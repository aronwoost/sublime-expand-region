import sublime, sublime_plugin, os

try:
  import expand_region_handler
except:
  from . import expand_region_handler

class ExpandRegionCommand(sublime_plugin.TextCommand):
  def run(self, edit, undo=False, debug=True):

    if (undo):
      string = self.view.substr(sublime.Region(0, self.view.size()))
      start = self.view.sel()[0].begin()
      end = self.view.sel()[0].end()
      result = expand_region_handler.undo(string, start, end, self.view.settings())
      if (result):
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(result["start"], result["end"]))
      return

    extension = ""
    if (self.view.file_name()):
      name, fileex = os.path.splitext(self.view.file_name())
      extension = fileex[1:]

    for region in self.view.sel():
      string = self.view.substr(sublime.Region(0, self.view.size()))
      start = region.begin()
      end = region.end()

      result = expand_region_handler.expand(string, start, end, extension, self.view.settings())
      if result:
        self.view.sel().add(sublime.Region(result["start"], result["end"]))
        if debug:
          print("startIndex: {0}, endIndex: {1}, type: {2}".format(result["start"], result["end"], result["type"]))

class ExpandRegionContext(sublime_plugin.EventListener):
    def on_query_context(self, view, key, *args):
      if key == "expand_region_soft_undo":
        item = view.command_history(0)
        if item[0] == "expand_region":
          return True

      return None