import sublime_plugin
from basic_expansions import foo

class ExpandRegionCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    foo();