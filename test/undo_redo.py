import unittest

from expand_region_handler import *

class UndoRedoTest(unittest.TestCase):

  def test_dont_crash_with_blank_json (self):
    settingsJson = ''
    newSettingsJson = add_to_stack(settingsJson, "teststring", 2, 3, 1, 1);
    newSettings = json.loads(newSettingsJson)
    self.assertEqual(newSettings.get("hash"), "d67c5cbf5b01c9f91932e3b8def5e5f8")
    self.assertEqual(newSettings.get("stack")[0].get("start"), 2)
    self.assertEqual(newSettings.get("stack")[0].get("end"), 3)

  def test_add_selection_as_only_item_in_stack_1 (self):
    settingsJson = '{"stack": [], "hash": ""}'
    newSettingsJson = add_to_stack(settingsJson, "teststring", 2, 3, 1, 1);
    newSettings = json.loads(newSettingsJson)
    self.assertEqual(newSettings.get("hash"), "d67c5cbf5b01c9f91932e3b8def5e5f8")
    self.assertEqual(newSettings.get("stack")[0].get("start"), 2)
    self.assertEqual(newSettings.get("stack")[0].get("end"), 3)

  def test_add_selection_as_only_item_in_stack_2 (self):
    settingsJson = '{"stack": [], "hash": "d67c5cbf5b01c9f91932e3b8def5e5f8"}'
    newSettingsJson = add_to_stack(settingsJson, "teststring", 2, 3, 1, 1);
    newSettings = json.loads(newSettingsJson)
    self.assertEqual(newSettings.get("hash"), "d67c5cbf5b01c9f91932e3b8def5e5f8")
    self.assertEqual(newSettings.get("stack")[0].get("start"), 2)
    self.assertEqual(newSettings.get("stack")[0].get("end"), 3)

  def test_add_selection_as_only_item_in_stack_3 (self):
    settingsJson = '{"hash": "d67c5cbf5b01c9f91932e3b8def5e5f8", "stack": [{"start": 2, "end": 3}]}'
    newSettingsJson = add_to_stack(settingsJson, "teststring1", 89, 99, 1, 1);
    newSettings = json.loads(newSettingsJson)
    self.assertEqual(newSettings.get("hash"), "790fabec68fa346d3444a3a2196b1741")
    self.assertEqual(newSettings.get("stack")[0].get("start"), 89)
    self.assertEqual(newSettings.get("stack")[0].get("end"), 99)

  def test_add_selection_as_only_item_in_stack_4 (self):
    settingsJson = '{"hash": "d67c5cbf5b01c9f91932e3b8def5e5f8", "stack": [{"start": 2, "end": 3}]}'
    newSettingsJson = add_to_stack(settingsJson, "teststring", 89, 99, 1, 1);
    newSettings = json.loads(newSettingsJson)
    self.assertEqual(newSettings.get("hash"), "d67c5cbf5b01c9f91932e3b8def5e5f8")
    self.assertEqual(newSettings.get("stack")[0].get("start"), 89)
    self.assertEqual(newSettings.get("stack")[0].get("end"), 99)

  def test_add_selection_to_existing_stack (self):
    settingsJson = '{"hash": "d67c5cbf5b01c9f91932e3b8def5e5f8", "stack": [{"start": 2, "end": 3}]}'
    newSettingsJson = add_to_stack(settingsJson, "teststring", 1, 4, 2, 3);
    newSettings = json.loads(newSettingsJson)
    self.assertEqual(newSettings.get("hash"), "d67c5cbf5b01c9f91932e3b8def5e5f8")
    self.assertEqual(newSettings.get("stack")[0].get("start"), 2)
    self.assertEqual(newSettings.get("stack")[0].get("end"), 3)
    self.assertEqual(newSettings.get("stack")[1].get("start"), 1)
    self.assertEqual(newSettings.get("stack")[1].get("end"), 4)

  def test_should_not_crash_with_umlaute (self):
    settingsJson = '{"hash": "", "stack": []}'
    newSettingsJson = add_to_stack(settingsJson, "hinzufügen", 1, 4, 2, 3);
    ## why the fuck is it working, it doesn't work in the IDE
    newSettings = json.loads(newSettingsJson)
    self.assertEqual(newSettings.get("hash"), "7f633295a95fdba4a07dcbe70d0768a0")
    self.assertEqual(newSettings.get("stack")[0].get("start"), 1)
    self.assertEqual(newSettings.get("stack")[0].get("end"), 4)

  ## undo

  def test_clear_stack_on_undo_because_string_is_different (self):
    settingsJson = '{"hash": "d67c5cbf5b01c9f91932e3b8def5e5f8", "stack": [{"start": 2, "end": 3}]}'
    result = get_last_selection(settingsJson, "teststring1", 2, 3);
    newSettings = json.loads(result["newSettingsJson"])
    self.assertEqual(newSettings.get("hash"), "790fabec68fa346d3444a3a2196b1741")
    self.assertEqual(len(newSettings.get("stack")), 0)

  def test_clear_stack_on_undo_because_selection_is_different (self):
    settingsJson = '{"hash": "d67c5cbf5b01c9f91932e3b8def5e5f8", "stack": [{"start": 2, "end": 3}, {"start": 1, "end": 4}]}'
    result = get_last_selection(settingsJson, "teststring", 89, 99);
    newSettings = json.loads(result["newSettingsJson"])
    self.assertEqual(newSettings.get("hash"), "d67c5cbf5b01c9f91932e3b8def5e5f8")
    self.assertEqual(len(newSettings.get("stack")), 0)

  def test_return_last_selection (self):
    settingsJson = '{"hash": "d67c5cbf5b01c9f91932e3b8def5e5f8", "stack": [{"start": 2, "end": 3}, {"start": 1, "end": 4}]}'
    result = get_last_selection(settingsJson, "teststring", 1, 4);
    newSelection = result["newSelection"]
    self.assertEqual(newSelection.get("startIndex"), 2)
    self.assertEqual(newSelection.get("endIndex"), 3)
    newSettings = json.loads(result["newSettingsJson"])
    self.assertEqual(newSettings.get("hash"), "d67c5cbf5b01c9f91932e3b8def5e5f8")
    self.assertEqual(len(newSettings.get("stack")), 1)
    self.assertEqual(newSettings.get("stack")[0].get("start"), 2)
    self.assertEqual(newSettings.get("stack")[0].get("end"), 3)

  def test_should_not_crash_when_stack_empty_1 (self):
    settingsJson = '{"stack": [], "hash": ""}'
    result = get_last_selection(settingsJson, "teststring", 1, 4);
    newSelection = result["newSelection"]
    self.assertEqual(newSelection, None)
    newSettings = json.loads(result["newSettingsJson"])
    self.assertEqual(newSettings.get("hash"), "d67c5cbf5b01c9f91932e3b8def5e5f8")
    self.assertEqual(len(newSettings.get("stack")), 0)

  def test_should_not_crash_when_stack_empty_2 (self):
    settingsJson = '{"stack": [], "hash": "d67c5cbf5b01c9f91932e3b8def5e5f8"}'
    result = get_last_selection(settingsJson, "teststring", 1, 4);
    newSelection = result["newSelection"]
    self.assertEqual(newSelection, None)
    newSettings = json.loads(result["newSettingsJson"])
    self.assertEqual(newSettings.get("hash"), "d67c5cbf5b01c9f91932e3b8def5e5f8")
    self.assertEqual(len(newSettings.get("stack")), 0)

  def test_should_not_crash_when_last_selection (self):
    settingsJson = '{"hash": "d67c5cbf5b01c9f91932e3b8def5e5f8", "stack": [{"start": 1, "end": 4}]}'
    result = get_last_selection(settingsJson, "teststring", 1, 4);
    newSelection = result["newSelection"]
    self.assertEqual(newSelection, None)
    newSettings = json.loads(result["newSettingsJson"])
    self.assertEqual(newSettings.get("hash"), "d67c5cbf5b01c9f91932e3b8def5e5f8")
    self.assertEqual(len(newSettings.get("stack")), 0)

if __name__ == "__main__":
  unittest.main()