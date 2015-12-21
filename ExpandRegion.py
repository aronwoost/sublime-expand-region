import sublime, sublime_plugin, os

try:
  import expand_region_handler
except:
  from . import expand_region_handler


def _detect_language(view, settings_name):
  point = view.sel()[0].b
  settings = sublime.load_settings(settings_name + ".sublime-settings")
  selectors = settings.get("scope_selectors")
  def maximal_score(scopes):
    if not scopes:  # validity check
      return 0
    return max(view.score_selector(point, s) for s in scopes)
  # calculate the maximal score for each language
  scores = [(k, maximal_score(v)) for k, v in selectors.items()]
  if not scores:  # validity check
    return
  # get the language with the best score
  scored_lang, score = max(scores, key=lambda item: item[1])
  language = scored_lang if score else ""
  return language


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
      language = (_detect_language(view, "ExpandRegion") or
                  _detect_language(view, "ExpandRegionFallback"))
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
