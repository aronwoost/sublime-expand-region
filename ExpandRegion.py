import sublime, sublime_plugin, os

try:
  import expand_region_handler
except:
  from . import expand_region_handler

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
  def run(self, edit, language="", undo=False, debug=False):
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


    # extract the locations from BracketHighlighter
    locations = view.settings().get("bracket_highlighter.locations", {})
    bh_regions = []
    if _ST3:
      for k, v in locations.get("open", {}).items():
        r_open = sublime.Region(*v)
        loc_close = locations.get("close", {})
        if k not in loc_close:
          continue
        close = loc_close[k]
        inner = sublime.Region(v[1], close[0])
        outer = sublime.Region(v[0], close[1])
        bh_regions.append((inner, outer))

    new_regions = []
    for region in self.view.sel():
      string = self.view.substr(sublime.Region(0, self.view.size()))
      start = region.begin()
      end = region.end()

      result = expand_region_handler.expand(string, start, end, language, self.view.settings())
      if result:
        if debug:
          print("startIndex: {0}, endIndex: {1}, type: {2}".format(result["start"], result["end"], result["type"]))
        result = sublime.Region(result["start"], result["end"])

      # if we are on ST2 or have no BracketHighlighter regions only work
      # with the result
      if not _ST3 or not bh_regions:
        if result:
          new_regions.append(result)
        else:
          # if there is no result, keep the current region
          new_regions.append(region)
      else:
        try:
          inner, outer = next(
            r for r in bh_regions
            if r[1].contains(region) and
            (region == r[0] or not region.contains(r[0]))
          )
          if inner == region:
            new_regions.append(outer)
          elif not result or (
              inner.begin() > result.begin() or inner.end() < result.end()):
            new_regions.append(inner)
          else:
            new_regions.append(result)
        except StopIteration:
          if not result:
            # if there is no result, keep the current region
            result = region
          new_regions.append(result)

    # replace the selections with the new regions
    view.sel().clear()
    for sel in new_regions:
      view.sel().add(sel)

    settings = sublime.load_settings("ExpandRegion.sublime-settings")
    do_force_enable_soft_undo = settings.get("force_soft_undo_integration")
    if do_force_enable_soft_undo:
      _force_enable_soft_undo(view, edit, new_regions)


class ExpandRegionContext(sublime_plugin.EventListener):
    def on_query_context(self, view, key, *args):
      if key == "expand_region_soft_undo":
        item = view.command_history(0)
        if item[0] == "expand_region":
          return True

      return None
