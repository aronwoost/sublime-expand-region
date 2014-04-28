import unittest

from expand_to_word import *

class WordTest(unittest.TestCase):

  @classmethod
  def setUpClass(self):
    with open ("test/snippets/word_01.txt", "r") as myfile:
      self.string1 = myfile.read()
    with open ("test/snippets/word_02.txt", "r") as myfile:
      self.string2 = myfile.read()

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

if __name__ == "__main__":
  unittest.main()