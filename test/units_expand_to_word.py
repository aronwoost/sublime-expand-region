import unittest

from expand_to_word import *

class WordTest(unittest.TestCase):

  @classmethod
  def setUpClass(self):
    with open ("test/snippets/word_01.txt", "r") as myfile:
      self.string1 = myfile.read()
    with open ("test/snippets/word_02.txt", "r") as myfile:
      self.string2 = myfile.read()
    with open ("test/snippets/word_03.txt", "r") as myfile:
      # decode utf8 unicode
      self.string3 = myfile.read().decode("utf8")

  def test_word_with_whitespaces_around (self):
    result = expand_to_word(" hello ", 3, 3);
    self.assertEqual(result["start"], 1)
    self.assertEqual(result["end"], 6)
    self.assertEqual(result["string"], "hello")

  def test_find_word_with_dot_before (self):
    result = expand_to_word("foo.bar", 5, 5);
    self.assertEqual(result["start"], 4)
    self.assertEqual(result["end"], 7)
    self.assertEqual(result["string"], "bar")

  def test_find_word_when_string_is_only_the_word (self):
    result = expand_to_word("bar", 1, 1);
    self.assertEqual(result["start"], 0)
    self.assertEqual(result["end"], 3)
    self.assertEqual(result["string"], "bar")

  def test_find_word_when_parts_of_the_word_are_already_selected (self):
    result = expand_to_word("hello", 1, 4);
    self.assertEqual(result["start"], 0)
    self.assertEqual(result["end"], 5)
    self.assertEqual(result["string"], "hello")

  def test_dont_find_word1 (self):
    result = expand_to_word(self.string1, 1, 10);
    self.assertEqual(result, None)

  def test_dont_find_word2 (self):
    result = expand_to_word(" ee ee", 2, 5);
    self.assertEqual(result, None)

  def test_dont_find_word3_and_dont_hang (self):
    result = expand_to_word("aaa", 0, 3);
    self.assertEqual(result, None)

  def test_dont_expand_to_linebreak (self):
    result = expand_to_word(self.string2, 0, 0);
    self.assertEqual(result, None)

  def test_special_chars1(self):
    result = expand_to_word(self.string3, 15, 15)
    self.assertEqual(result["start"], 13)
    self.assertEqual(result["end"], 24)

  def test_special_chars2(self):
    result = expand_to_word(self.string3, 57, 57)
    self.assertEqual(result["start"], 57)
    self.assertEqual(result["end"], 64)

  def test_special_chars3(self):
    result = expand_to_word(self.string3, 75, 77)
    self.assertEqual(result["start"], 75)
    self.assertEqual(result["end"], 85)

  def test_special_chars4(self):
    result = expand_to_word(self.string3, 89, 89)
    self.assertEqual(result["start"], 86)
    self.assertEqual(result["end"], 89)

if __name__ == "__main__":
  unittest.main()