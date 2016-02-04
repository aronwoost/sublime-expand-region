import re, hashlib, json

try:
  import javascript
  import html
  import latex
  import python
except:
  from . import javascript
  from . import html
  from . import latex
  from . import python

def expand(string, start, end, language="", settings=None):

  if language == "html":
    result = html.expand(string, start, end)
  elif language == "latex":
    result = latex.expand(string, start, end)
  elif language == "python":
    result = python.expand(string, start, end)
  else:
    result = javascript.expand(string, start, end)

  if (result != None and settings):
    expand_region_settings = settings.get("expand_region_settings")
    newSettingsJson = add_to_stack(expand_region_settings, string.encode('utf-8'), result.get("start"), result.get("end"), start, end)
    print(newSettingsJson)
    settings.set("expand_region_settings", newSettingsJson)

  return result;

def undo(string, start, end, settings=None):

  if (settings):
    expand_region_settings = settings.get("expand_region_settings")
    result = get_last_selection(expand_region_settings, string.encode('utf-8'), start, end)
    print(result.get("newSettingsJson"))
    settings.set("expand_region_settings", result.get("newSettingsJson"))
    if (result.get("newSelection") == None):
      return None
    return {"start": result.get("newSelection").get("startIndex"), "end": result.get("newSelection").get("endIndex")}


def add_to_stack(settingsJson, string, startIndex, endIndex, oldStartIndex, oldEndIndex):
  if (settingsJson == "" or settingsJson == None):
    settingsJson = '{"stack": [], "hash": ""}'
  settings = json.loads(settingsJson)
  lastStackItem = None
  if (settings.get("stack") and len(settings.get("stack")) > 0):
    lastStackItem = settings.get("stack")[len(settings.get("stack")) -1]
  else:
    lastStackItem = {"start": -1, "end": -1}
  stringHash = hashlib.md5(string).hexdigest()
  if (stringHash != settings.get("hash")):
    settings["hash"] = stringHash
    settings["stack"] = [{"start": startIndex, "end": endIndex}]
  elif (stringHash == settings.get("hash") and (lastStackItem.get("start") != oldStartIndex or lastStackItem.get("end") != oldEndIndex)):
    settings["stack"] = [{"start": startIndex, "end": endIndex}]
  elif (stringHash == settings.get("hash")):
    settings["stack"].append({"start": startIndex, "end": endIndex})
  newSettingsJson = json.dumps(settings)
  return newSettingsJson

def get_last_selection(settingsJson, string, startIndex, endIndex):
  settings = json.loads(settingsJson)
  newSelection = None
  lastStackItem = None
  if (settings.get("stack") and len(settings.get("stack")) > 0):
    lastStackItem = settings.get("stack")[len(settings.get("stack")) -1]
  else:
    lastStackItem = {"start": -1, "end": -1}
  newSelection = None
  stringHash = hashlib.md5(string).hexdigest()
  if (stringHash != settings.get("hash")):
    settings["hash"] = stringHash
    settings["stack"] = []
  elif (stringHash == settings.get("hash") and (lastStackItem.get("start") != startIndex or lastStackItem.get("end") != endIndex)):
    settings["hash"] = stringHash
    settings["stack"] = []
  elif (stringHash == settings.get("hash") and lastStackItem.get("start") == startIndex and lastStackItem.get("end") == endIndex):
    settings.get("stack").pop()
    if (len(settings.get("stack")) > 0):
      lastStackItem = settings.get("stack")[len(settings.get("stack")) -1]
      newSelection = {"startIndex": lastStackItem.get("start"), "endIndex": lastStackItem.get("end")}
  newSettingsJson = json.dumps(settings)
  return {"newSettingsJson": newSettingsJson, "newSelection": newSelection}




