import unittest

from utils import *

class UtilsTest(unittest.TestCase):

  @classmethod
  def setUpClass(self):
    with open ("test/snippets/linebreak_01.txt", "r") as myfile:
      self.string1 = myfile.read()

  def test_find_linebreak (self):
    self.assertTrue(selection_contain_linebreaks(self.string1, 0, 8))

  def test_dont_find_linebreak (self):
    self.assertFalse(selection_contain_linebreaks("aaa", 1, 2))


class GetLineTest(unittest.TestCase):

  @classmethod
  def setUpClass(self):
    with open ("test/snippets/line_01.txt", "r") as myfile:
      self.string1 = myfile.read()

  def test_get_line (self):
    result = get_line(self.string1, 13, 13);
    self.assertEqual(result["start"], 8)
    self.assertEqual(result["end"], 18)


class TrimTest(unittest.TestCase):

  @classmethod
  def setUpClass(self):
    with open ("test/snippets/trim_01.txt", "r") as myfile:
      self.string1 = myfile.read()
    with open ("test/snippets/trim_02.txt", "r") as myfile:
      self.string2 = myfile.read()

  def test_1 (self):
    result = trim("  aa  ");
    self.assertEqual(result["start"], 2)
    self.assertEqual(result["end"], 4)

  def test_2 (self):
    result = trim("  'a a'  ");
    self.assertEqual(result["start"], 2)
    self.assertEqual(result["end"], 7)

  def test_3 (self):
    result = trim(self.string1);
    self.assertEqual(result["start"], 2)
    self.assertEqual(result["end"], 11)

  def test_4 (self):
    result = trim(" foo.bar['property'].getX()");
    self.assertEqual(result["start"], 1)
    self.assertEqual(result["end"], 27)

  def test_5 (self):
    result = trim(self.string2);
    self.assertEqual(result["start"], 2)
    self.assertEqual(result["end"], 49)


if __name__ == "__main__":
  unittest.main()