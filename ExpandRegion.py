import sublime, sublime_plugin, os

try:
  import expand_region_handler
except:
  from . import expand_region_handler

class ExpandRegionCommand(sublime_plugin.TextCommand):
  def run(self, edit, undo=False, debug=True):
    view = self.view

    if (undo):
      string = view.substr(sublime.Region(0, view.size()))
      start = view.sel()[0].begin()
      end = view.sel()[0].end()
      result = expand_region_handler.undo(string, start, end, view.settings())
      if (result):
        view.sel().clear()
        view.sel().add(sublime.Region(result["start"], result["end"]))
      return

    language = ""
    point = view.sel()[0].b
    if view.score_selector(point, "text.html") or view.score_selector(point, "text.xml"):
      language = "html"
    elif view.score_selector(point, "source.python") or view.score_selector(point, "source.cython"):
      language = "python"
    elif view.score_selector(point, "text.tex"):
      language = "tex"

    for region in view.sel():
      string = view.substr(sublime.Region(0, view.size()))
      start = region.begin()
      end = region.end()

      result = expand_region_handler.expand(string, start, end, language, view.settings())
      if result:
        view.sel().add(sublime.Region(result["start"], result["end"]))
        if debug:
          print("startIndex: {0}, endIndex: {1}, type: {2}".format(result["start"], result["end"], result["type"]))

class ExpandRegionContext(sublime_plugin.EventListener):
    def on_query_context(self, view, key, *args):
      if key == "expand_region_soft_undo":
        item = view.command_history(0)
        if item[0] == "expand_region":
          return True

      return None
