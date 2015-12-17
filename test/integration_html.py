import unittest

from expand_region_handler import *

class HtmlIntegrationTest(unittest.TestCase):

  @classmethod
  def setUpClass(self):
    with open ("test/snippets/html_01.txt", "r") as myfile:
      self.string1 = myfile.read()

  def test_expand_to_inner_head_of_node2 (self):
    result = expand(self.string1, 11, 15, "html")
    self.assertEqual(result["start"], 9)
    self.assertEqual(result["end"], 19)

  def test_expand_to_inner_head_of_node3 (self):
    result = expand(self.string1, 162, 164, "html")
    self.assertEqual(result["start"], 161)
    self.assertEqual(result["end"], 164)

  def test_expand_to_head_of_node1 (self):
    result = expand("  <div>test</div>", 3, 6, "html")
    self.assertEqual(result["start"], 2)
    self.assertEqual(result["end"], 7)

  def test_expand_to_head_of_node2 (self):
    result = expand(self.string1, 9, 19, "html")
    self.assertEqual(result["start"], 8)
    self.assertEqual(result["end"], 20)

  def test_expand_to_head_of_node3 (self):
    result = expand(self.string1, 161, 164, "html")
    self.assertEqual(result["start"], 160)
    self.assertEqual(result["end"], 165)

  def test_expand_to_complete_node1 (self):
    result = expand("  <div>test</div>", 2, 7, "html")
    self.assertEqual(result["start"], 2)
    self.assertEqual(result["end"], 17)

  def test_expand_to_complete_node2 (self):
    result = expand(self.string1, 8, 20, "html")
    self.assertEqual(result["start"], 8)
    self.assertEqual(result["end"], 172)

  def test_expand_to_complete_node3 (self):
    result = expand(self.string1, 160, 165, "html")
    self.assertEqual(result["start"], 152)
    self.assertEqual(result["end"], 165)

  def test_expand_to_content_of_parent_node1 (self):
    result = expand(self.string1, 147, 147, "html")
    self.assertEqual(result["start"], 20)
    self.assertEqual(result["end"], 168)

  def test_expand_to_content_of_parent_node2 (self):
    result = expand(self.string1, 20, 168, "html")
    self.assertEqual(result["start"], 8)
    self.assertEqual(result["end"], 172)

  def test_expand_to_inner_self_closing_node1 (self):
    result = expand("<input value='test'>", 1, 6, "html")
    self.assertEqual(result["start"], 1)
    self.assertEqual(result["end"], 19)

  def test_expand_to_inner_self_closing_node2 (self):
    result = expand("<magic value='test' />", 1, 6, "html")
    self.assertEqual(result["start"], 1)
    self.assertEqual(result["end"], 21)

  def test_expand_to_self_closing_node1 (self):
    result = expand("<input value='test'>", 1, 19, "html")
    self.assertEqual(result["start"], 0)
    self.assertEqual(result["end"], 20)

  def test_expand_to_self_closing_node2 (self):
    result = expand("<magic value='test' />", 1, 21, "html")
    self.assertEqual(result["start"], 0)
    self.assertEqual(result["end"], 22)

if __name__ == "__main__":
  unittest.main()
