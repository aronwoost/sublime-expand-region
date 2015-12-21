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

    new_regions = []
    for region in self.view.sel():
      string = self.view.substr(sublime.Region(0, self.view.size()))
      start = region.begin()
      end = region.end()

      result = expand_region_handler.expand(string, start, end, language, self.view.settings())
      if result:
        new_regions.append(sublime.Region(result["start"], result["end"]))
        if debug:
          print("startIndex: {0}, endIndex: {1}, type: {2}".format(result["start"], result["end"], result["type"]))
      else:
        # if there is no result, keep the current region
        new_regions.append(region)

    # replace the selections with the new regions
    view.sel().clear()
    for sel in new_regions:
      view.sel().add(sel)

    # TODO take this from the settings
    do_force_enable_soft_undo = True
    if do_force_enable_soft_undo:
      _force_enable_soft_undo(view, edit, new_regions)


class ExpandRegionContext(sublime_plugin.EventListener):
    def on_query_context(self, view, key, *args):
      if key == "expand_region_soft_undo":
        item = view.command_history(0)
        if item[0] == "expand_region":
          return True

      return None
