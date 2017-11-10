import sublime, sublime_plugin, os

try:
  import expand_region_handler
  import utils
except:
  from . import expand_region_handler
  from . import utils

# get the used sublime text version
_ST3 = sublime.version() >= '3000'

if _ST3:
  def _force_enable_soft_undo(view, edit, new_regions):
    # end the current edit
    view.end_edit(edit)
    # this is a hack to enable soft_undo
    # the entry in soft undo seems to be forced if we change the selection
    # with a token, that has a different id.
    # Hence just use the (invalid) id = -1.
    subedit = view.begin_edit(-1, "expand_region_force_enable_soft_undo")
    try:
      for sel in new_regions:
        view.sel().add(sel)
    finally:
      view.end_edit(subedit)
else:  # ST2
  def _force_enable_soft_undo(view, edit, new_regions):
    # end the current edit
    view.end_edit(edit)
    # force enable soft-undo by starting a new edit with a different name
    subedit = view.begin_edit("expand_region_force_enable_soft_undo")
    view.end_edit(subedit)


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
    utils.is_debug_enabled = debug

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
      print("ExpandRegion, ExpandRegion.py, Determined language: '{0}'".format(language))

    new_regions = []
    is_region_expanded = True
    for region in self.view.sel():
      string = self.view.substr(sublime.Region(0, self.view.size()))
      start = region.begin()
      end = region.end()

      result = expand_region_handler.expand(string, start, end, language, self.view.settings())
      if result:
        new_regions.append(sublime.Region(result["start"], result["end"]))
        if debug:
          print("ExpandRegion, ExpandRegion.py, startIndex: {0}, endIndex: {1}, type: {2}".format(result["start"], result["end"], result["type"]))
      else:
        # if there is no result, call the built-in sublime text expand_selection to scope command
        is_region_expanded = False

    if is_region_expanded:
      # replace the selections with the new regions
      view.sel().clear()
      for sel in new_regions:
        view.sel().add(sel)

      settings = sublime.load_settings("ExpandRegion.sublime-settings")
      do_force_enable_soft_undo = settings.get("force_soft_undo_integration")
      if do_force_enable_soft_undo:
        _force_enable_soft_undo(view, edit, new_regions)
    else:
      if debug:
        print( "ExpandRegion, ExpandRegion.py, calling Sublime Text expand_selection to scope..." )
      view.run_command( "expand_selection", {"to": "scope"} )


class ExpandRegionContext(sublime_plugin.EventListener):
    def on_query_context(self, view, key, *args):
      if key == "expand_region_soft_undo":
        item = view.command_history(0)
        if item[0] == "expand_region":
          return True

      return None
