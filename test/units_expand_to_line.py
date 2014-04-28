import unittest

from expand_to_line import *

class ExpandToLineTest(unittest.TestCase):

  @classmethod
  def setUpClass(self):
    with open ("test/snippets/line_01.txt", "r") as myfile:
      self.string1 = myfile.read()
    with open ("test/snippets/line_02.txt", "r") as myfile:
      self.string2 = myfile.read()

  def test_with_spaces_at_beginning (self):
    result = expand_to_line(self.string1, 10, 16);
    self.assertEqual(result["string"], "is it me")
    self.assertEqual(result["start"], 10)
    self.assertEqual(result["end"], 18)

  def test_existing_line_selection (self):
    result = expand_to_line(self.string1, 10, 18);
    self.assertEqual(result, None)

  def test_with_no_spaces_or_tabs_at_beginning (self):
    result = expand_to_line(self.string2, 6, 12);
    self.assertEqual(result["string"], "is it me")
    self.assertEqual(result["start"], 6)
    self.assertEqual(result["end"], 14)

  def test_with_indention (self):
    result = expand_to_line(" aa", 0, 0);
    self.assertEqual(result["string"], " aa")
    self.assertEqual(result["start"], 0)
    self.assertEqual(result["end"], 3)

  def test_without_indention (self):
    result = expand_to_line(" aa", 1, 1);
    self.assertEqual(result["string"], "aa")
    self.assertEqual(result["start"], 1)
    self.assertEqual(result["end"], 3)

  def test_with_indention2 (self):
    result = expand_to_line("  aa", 1, 1);
    self.assertEqual(result["string"], "  aa")
    self.assertEqual(result["start"], 0)
    self.assertEqual(result["end"], 4)

if __name__ == "__main__":
  unittest.main()