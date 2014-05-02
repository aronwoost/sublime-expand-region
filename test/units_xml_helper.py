import unittest

from expand_to_xml_node import *

class XmlHelperTest(unittest.TestCase):

  def test_within_node_true (self):
    result = is_within_tag("<input>", 2, 2)
    self.assertEqual(result["start"], 0)
    self.assertEqual(result["end"], 7)

  def test_within_node_false1 (self):
    result = is_within_tag(">input<", 2, 2)
    self.assertEqual(result, False)

  def test_within_node_false2 (self):
    result = is_within_tag("input", 2, 2)
    self.assertEqual(result, False)

  def test_get_tag_name1 (self):
    result = get_tag_properties("<input class='test'>")
    self.assertEqual(result["name"], "input")
    self.assertEqual(result["type"], "self_closing")

  def test_get_tag_name2 (self):
    result = get_tag_properties("< input class='test'>")
    self.assertEqual(result["name"], "input")

  def test_get_tag_name3 (self):
    result = get_tag_properties("<  input class='test'>")
    self.assertEqual(result["name"], "input")

  def test_get_tag_name4 (self):
    result = get_tag_properties("<input>")
    self.assertEqual(result["name"], "input")

  def test_get_tag_name5 (self):
    result = get_tag_properties("</input>")
    self.assertEqual(result["name"], "input")
    self.assertEqual(result["type"], "closing")

  def test_get_tag_name6 (self):
    result = get_tag_properties("<magic />")
    self.assertEqual(result["name"], "magic")
    self.assertEqual(result["type"], "self_closing")

  def test_get_tag_name7 (self):
    result = get_tag_properties("<div>")
    self.assertEqual(result["name"], "div")
    self.assertEqual(result["type"], "opening")

  def test_find_closing_tag1 (self):
    result = find_tag("<div>test</div></div>", "forward", "div")
    self.assertEqual(result["start"], 15)
    self.assertEqual(result["end"], 21)

  def test_find_closing_tag2 (self):
    result = find_tag("test</div>", "forward", "div")
    self.assertEqual(result["start"], 4)
    self.assertEqual(result["end"], 10)

  def test_find_opening_tag1 (self):
    result = find_tag("  <div><div>test</div>", "backward", "div")
    self.assertEqual(result["start"], 2)
    self.assertEqual(result["end"], 7)

  def test_find_previous_open_tag1 (self):
    result = find_tag("<div></div><div><a href='#'></a>", "backward")
    self.assertEqual(result["start"], 11)
    self.assertEqual(result["end"], 16)
    self.assertEqual(result["name"], "div")

  def test_find_previous_open_tag2 (self):
    result = find_tag("<div></div><div style='color: red;'><a href='#'></a>", "backward")
    self.assertEqual(result["start"], 11)
    self.assertEqual(result["end"], 36)
    self.assertEqual(result["name"], "div")

  def test_find_previous_open_tag3 (self):
    result = find_tag("<div><img />", "backward")
    self.assertEqual(result["start"], 0)
    self.assertEqual(result["end"], 5)
    self.assertEqual(result["name"], "div")

  def test_find_previous_open_tag4 (self):
    result = find_tag("<div><img>", "backward")
    self.assertEqual(result["start"], 0)
    self.assertEqual(result["end"], 5)
    self.assertEqual(result["name"], "div")

if __name__ == "__main__":
  unittest.main()