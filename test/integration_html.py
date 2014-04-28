import unittest

from expand_region_handler import *

class HtmlIntegrationTest(unittest.TestCase):

  @classmethod
  def setUpClass(self):
    with open ("test/snippets/html_01.txt", "r") as myfile:
      self.string1 = myfile.read()

  def test_expand_to_complete_node1 (self):
    result = expand("  <div>test</div>", 3, 6, "html")
    self.assertEqual(result["start"], 2)
    self.assertEqual(result["end"], 17)

  def test_expand_to_complete_node2 (self):
    result = expand(self.string1, 11, 15, "html")
    self.assertEqual(result["start"], 8)
    self.assertEqual(result["end"], 172)

  def test_expand_to_complete_node3 (self):
    result = expand(self.string1, 162, 164, "html")
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
if __name__ == "__main__":
  unittest.main()