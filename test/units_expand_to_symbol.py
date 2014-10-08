import unittest

from expand_to_symbols import *

class ExpandToSymbolTest(unittest.TestCase):

  @classmethod
  def setUpClass(self):
    with open ("test/snippets/symbol_01.txt", "r") as myfile:
      self.string1 = myfile.read()
    with open ("test/snippets/symbol_02.txt", "r") as myfile:
      self.string2 = myfile.read()
    with open ("test/snippets/symbol_03.txt", "r") as myfile:
      self.string3 = myfile.read()

  def test_symbol_inner (self):
    result = expand_to_symbols(self.string1, 7, 10);
    self.assertEqual(result["start"], 1)
    self.assertEqual(result["end"], 10)
    self.assertEqual(result["string"], "foo - bar")

  def test_symbol_outer (self):
    result = expand_to_symbols(self.string1, 1, 10);
    self.assertEqual(result["start"], 0)
    self.assertEqual(result["end"], 11)
    self.assertEqual(result["string"], "(foo - bar)")

  def test_look_back_dont_hang (self):
    result = expand_to_symbols("   ", 1, 2);
    self.assertEqual(result, None)

  def test_look_ahead_dont_hang (self):
    result = expand_to_symbols("(   ", 2, 2);
    self.assertEqual(result, None)

  def test_fix_look_back (self):
    result = expand_to_symbols(self.string2, 32, 32);
    self.assertEqual(result["start"], 12)
    self.assertEqual(result["end"], 35)
    self.assertEqual(result["string"], "foo.indexOf('bar') > -1")

  def test_respect_symbols_in_selection1 (self):
    result = expand_to_symbols("(a['value'])", 6, 11);
    self.assertEqual(result["start"], 1)
    self.assertEqual(result["end"], 11)
    # self.assertEqual(result["string"], "foo.indexOf('bar') > -1")

  def test_respect_symbols_in_selection (self):
    result = expand_to_symbols(self.string3, 10, 61);
    self.assertEqual(result["start"], 5)
    self.assertEqual(result["end"], 66)
    # self.assertEqual(result["string"], "foo.indexOf('bar') > -1")

  def test_ignore_symbols_in_strings (self):
    result = expand_to_symbols("{'a(a'+bb+'c)c'}", 8, 8);
    self.assertEqual(result["start"], 1)
    self.assertEqual(result["end"], 15)
    self.assertEqual(result["type"], "symbol")

if __name__ == "__main__":
  unittest.main()