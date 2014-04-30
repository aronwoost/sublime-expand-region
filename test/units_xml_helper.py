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
    self.assertEqual(result["has_closing_slash"], True)

  def test_sanitize_tag1 (self):
    result = sanitize_tag_chars("<div>")
    self.assertEqual(result, "<>")

  def test_sanitize_tag2 (self):
    result = sanitize_tag_chars("<div style='color: red;'>")
    self.assertEqual(result, "<>")

  def test_sanitize_tag3 (self):
    result = sanitize_tag_chars("</div>")
    self.assertEqual(result, "</>")

  def test_get_closing_tag1 (self):
    result = get_closing_tag("<div><div>test</div></div>", "div")
    self.assertEqual(result["start"], 20)
    self.assertEqual(result["end"], 26)

  def test_get_closing_tag2 (self):
    result = get_closing_tag("<div style='color: red;'>test</div>", "div")
    self.assertEqual(result["start"], 29)
    self.assertEqual(result["end"], 35)

  def test_get_opening_tag1 (self):
    result = get_opening_tag("  <div><div>test</div></div>", "div")
    self.assertEqual(result["start"], 2)
    self.assertEqual(result["end"], 7)

  def test_find_previous_open_tag1 (self):
    result = find_parent_open_tag("<div></div><div><a href='#'></a>")
    self.assertEqual(result["start"], 11)
    self.assertEqual(result["end"], 16)
    self.assertEqual(result["name"], "div")

  def test_find_previous_open_tag2 (self):
    result = find_parent_open_tag("<div></div><div style='color: red;'><a href='#'></a>")
    self.assertEqual(result["start"], 11)
    self.assertEqual(result["end"], 36)
    self.assertEqual(result["name"], "div")
if __name__ == "__main__":
  unittest.main()