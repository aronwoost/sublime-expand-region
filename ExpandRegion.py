import sublime, sublime_plugin, os

try:
  import expand_region_handler
except:
  from . import expand_region_handler

class ExpandRegionCommand(sublime_plugin.TextCommand):
  def run(self, edit, language="", undo=False, debug=True):
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

    if not language:
      point = view.sel()[0].b
      settings = sublime.load_settings("ExpandRegion.sublime-settings")
      selectors = settings.get("scope_selectors")
      def maximal_score(scopes):
        return max(view.score_selector(point, s) for s in scopes)
      # calculate the maximal score for each language
      scores = [(k, maximal_score(v)) for k, v in selectors.items()]
      # get the language with the best score
      scored_lang, score = max(scores, key=lambda item: item[1])
      language = scored_lang if score else ""
    if debug:
      print("Determined language: '{0}'".format(language))

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
