import unittest

from expand_to_word_with_dots import *

class WordWithDotsTest(unittest.TestCase):
  def test (self):
    result = expand_to_word_with_dots("foo.bar", 6, 7);
    self.assertEqual(result["start"], 0)
    self.assertEqual(result["end"], 7)
    self.assertEqual(result["string"], "foo.bar")

if __name__ == "__main__":
  unittest.main()