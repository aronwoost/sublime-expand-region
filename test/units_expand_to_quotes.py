import unittest

from expand_to_quotes import *

class ExpandToQuotesTest(unittest.TestCase):

  @classmethod
  def setUpClass(self):
    with open ("test/snippets/quote_01.txt", "r") as myfile:
      self.string1 = myfile.read()
    with open ("test/snippets/quote_02.txt", "r") as myfile:
      self.string2 = myfile.read()
    with open ("test/snippets/quote_03.txt", "r") as myfile:
      self.string3 = myfile.read()

  def test_double_quotes_inner (self):
    result = expand_to_quotes(self.string1, 6, 12);
    self.assertEqual(result["start"], 1)
    self.assertEqual(result["end"], 12)
    self.assertEqual(result["string"], "test string")

  def test_double_quotes_outer (self):
    result = expand_to_quotes(self.string1, 1, 12);
    self.assertEqual(result["start"], 0)
    self.assertEqual(result["end"], 13)
    self.assertEqual(result["string"], "\"test string\"")

  def test_single_quotes_inner (self):
    result = expand_to_quotes(self.string2, 6, 12);
    self.assertEqual(result["start"], 1)
    self.assertEqual(result["end"], 12)
    self.assertEqual(result["string"], "test string")

  def test_single_quotes_outer (self):
    result = expand_to_quotes(self.string2, 1, 12);
    self.assertEqual(result["start"], 0)
    self.assertEqual(result["end"], 13)
    self.assertEqual(result["string"], "'test string'")

  def test_should_not_find1 (self):
    result = expand_to_quotes(" ': '", 1, 1);
    self.assertEqual(result, None)

  def test_should_not_find2 (self):
    result = expand_to_quotes("': '", 4, 4);
    self.assertEqual(result, None)

  def test_ignore_escaped_quotes (self):
    result = expand_to_quotes(self.string3, 2, 2);
    self.assertEqual(result["start"], 1)
    self.assertEqual(result["end"], 13)
    self.assertEqual(result["string"], "test\\\"string")

if __name__ == "__main__":
  unittest.main()