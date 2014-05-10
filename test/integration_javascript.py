import unittest

from expand_region_handler import *

class JavascriptIntegrationTest(unittest.TestCase):

  @classmethod
  def setUpClass(self):
    with open ("test/snippets/integration_01.txt", "r") as myfile:
      self.string1 = myfile.read()
    with open ("test/snippets/integration_02.txt", "r") as myfile:
      self.string2 = myfile.read()
    with open ("test/snippets/integration_03.txt", "r") as myfile:
      self.string3 = myfile.read()
    with open ("test/snippets/integration_04.txt", "r") as myfile:
      self.string4 = myfile.read()

  def test_word (self):
    result = expand(self.string1, 7, 7);
    self.assertEqual(result["start"], 6)
    self.assertEqual(result["end"], 9)
    self.assertEqual(result["string"], "bar")
    self.assertEqual(result["type"], "word")
    self.assertEqual(result["expand_stack"], ["word"])

  def test_quotes_inner (self):
    result = expand(self.string1, 6, 9);
    self.assertEqual(result["start"], 2)
    self.assertEqual(result["end"], 9)
    self.assertEqual(result["string"], "foo bar")
    self.assertEqual(result["type"], "quotes")
    self.assertEqual(result["expand_stack"], ["word", "quotes"])

  def test_quotes_outer (self):
    result = expand(self.string1, 2, 9);
    self.assertEqual(result["start"], 1)
    self.assertEqual(result["end"], 10)
    self.assertEqual(result["string"], "\"foo bar\"")
    self.assertEqual(result["type"], "quotes")
    self.assertEqual(result["expand_stack"], ["word", "quotes"])

  def test_symbol_inner (self):
    result = expand(self.string1, 1, 10);
    self.assertEqual(result["start"], 1)
    self.assertEqual(result["end"], 16)
    self.assertEqual(result["string"], "\"foo bar\" + \"x\"")
    self.assertEqual(result["type"], "semantic_unit")
    self.assertEqual(result["expand_stack"], ["word", "quotes", "semantic_unit"])

  def test_dont_expand_to_dots (self):
    result = expand(self.string2, 2, 5);
    self.assertEqual(result["start"], 1)
    self.assertEqual(result["end"], 10)
    self.assertEqual(result["string"], " foo.bar ")
    self.assertEqual(result["type"], "quotes")
    self.assertEqual(result["expand_stack"], ["word", "quotes"])

  # def test_expand_to_line (self):
  #   result = expand(self.string3, 30, 35);
  #   self.assertEqual(result["start"], 28)
  #   self.assertEqual(result["end"], 37)
  #   self.assertEqual(result["string"], "foo: true")
  #   self.assertEqual(result["type"], "line")
  #   self.assertEqual(result["expand_stack"], ["word", "quotes", "semantic_unit", "symbols", "line"])

  def test_expand_to_symbol_from_line (self):
    result = expand(self.string3, 28, 37);
    self.assertEqual(result["start"], 23)
    self.assertEqual(result["end"], 40)
    self.assertEqual(result["string"], "\n    foo: true\n  ")
    self.assertEqual(result["type"], "symbol")
    self.assertEqual(result["expand_stack"], ["semantic_unit", "symbols"])

  def test_skip_some_because_of_linebreak (self):
    result = expand(self.string3, 22, 41);
    self.assertEqual(result["start"], 15)
    self.assertEqual(result["end"], 41)
    self.assertEqual(result["string"], "return {\n    foo: true\n  }")
    self.assertEqual(result["type"], "semantic_unit")
    self.assertEqual(result["expand_stack"], ["semantic_unit"])

  def test_skip_some_because_of_linebreak_2 (self):
    result = expand(self.string3, 15, 41);
    self.assertEqual(result["start"], 12)
    self.assertEqual(result["end"], 42)
    self.assertEqual(result["type"], "symbol")
    self.assertEqual(result["expand_stack"], ["semantic_unit", "symbols"])

  def test_symbols_in_string_01 (self):
    result = expand(self.string4, 35, 42);
    self.assertEqual(result["start"], 30)
    self.assertEqual(result["end"], 42)
    self.assertEqual(result["type"], "semantic_unit")
    self.assertEqual(result["expand_stack"], ["semantic_unit"])

  def test_symbols_in_string_02 (self):
    result = expand(self.string4, 30, 42);
    self.assertEqual(result["start"], 29)
    self.assertEqual(result["end"], 43)
    self.assertEqual(result["type"], "symbol")
    self.assertEqual(result["expand_stack"], ["semantic_unit", "symbols"])

  def test_symbols_in_string_03 (self):
    result = expand(self.string4, 29, 43);
    self.assertEqual(result["start"], 29)
    self.assertEqual(result["end"], 46)
    self.assertEqual(result["type"], "semantic_unit")
    self.assertEqual(result["expand_stack"], ["semantic_unit"])

  def test_symbols_in_string_04 (self):
    result = expand(self.string4, 29, 46);
    self.assertEqual(result["start"], 28)
    self.assertEqual(result["end"], 47)
    self.assertEqual(result["type"], "symbol")
    self.assertEqual(result["expand_stack"], ["semantic_unit", "symbols"])

  def test_symbols_in_string_05 (self):
    result = expand(self.string4, 28, 47);
    self.assertEqual(result["start"], 23)
    self.assertEqual(result["end"], 55)
    self.assertEqual(result["type"], "quotes")
    self.assertEqual(result["expand_stack"], ["word", "quotes"])

if __name__ == "__main__":
  unittest.main()