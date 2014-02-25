import unittest
import expand_region_handler

class WordTest(unittest.TestCase):
  def setUp(self):
    with open ("test/word_01.txt", "r") as myfile:
      self.string1 = myfile.read()

  def test_word_with_whitespaces_around (self):
    result = expand_region_handler.expand_to_word(" hello ", 3, 3);
    self.assertEqual(result["start"], 1)
    self.assertEqual(result["end"], 6)
    self.assertEqual(result["string"], "hello")

  def test_dont_find_word (self):
    result = expand_region_handler.expand_to_word(self.string1, 1, 10);
    self.assertEqual(result, None)

  def test_dont_find_word2 (self):
    result = expand_region_handler.expand_to_word(" ee ee", 2, 5);
    self.assertEqual(result, None)

  def test_string_is_only_word (self):
    result = expand_region_handler.expand_to_word("bar", 1, 1);
    self.assertEqual(result["start"], 0)
    self.assertEqual(result["end"], 3)
    self.assertEqual(result["string"], "bar")

  def test_dont_find_word3 (self):
    result = expand_region_handler.expand_to_word("foo.bar", 5, 5);
    self.assertEqual(result["start"], 4)
    self.assertEqual(result["end"], 7)
    self.assertEqual(result["string"], "bar")

  def test_dont_find_word3_and_dont_hang (self):
    result = expand_region_handler.expand_to_word("aaa", 0, 3);
    self.assertEqual(result, None)

class WordWithDotsTest(unittest.TestCase):
  def test (self):
    result = expand_region_handler.expand_to_word_with_dots("foo.bar", 6, 7);
    self.assertEqual(result["start"], 0)
    self.assertEqual(result["end"], 7)
    self.assertEqual(result["string"], "foo.bar")

class LineTest(unittest.TestCase):
  def setUp(self):
    with open ("test/line_01.txt", "r") as myfile:
      self.string1 = myfile.read()
    with open ("test/line_02.txt", "r") as myfile:
      self.string2 = myfile.read()

  def test_with_spaces_at_beginning (self):
    result = expand_region_handler.expand_to_line(self.string1, 10, 16);
    self.assertEqual(result["string"], "is it me")
    self.assertEqual(result["start"], 10)
    self.assertEqual(result["end"], 18)

  def test_with_no_spaces_or_tabs_at_beginning (self):
    result = expand_region_handler.expand_to_line(self.string2, 6, 12);
    self.assertEqual(result["string"], "is it me")
    self.assertEqual(result["start"], 6)
    self.assertEqual(result["end"], 14)

class QuoteTest(unittest.TestCase):
  def setUp(self):
    with open ("test/quote_01.txt", "r") as myfile:
      self.string1 = myfile.read()
    with open ("test/quote_02.txt", "r") as myfile:
      self.string2 = myfile.read()

  def test_double_quotes_inner (self):
    result = expand_region_handler.expand_to_quotes(self.string1, 6, 12);
    self.assertEqual(result["start"], 1)
    self.assertEqual(result["end"], 12)
    self.assertEqual(result["string"], "test string")

  def test_double_quotes_outer (self):
    result = expand_region_handler.expand_to_quotes(self.string1, 1, 12);
    self.assertEqual(result["start"], 0)
    self.assertEqual(result["end"], 13)
    self.assertEqual(result["string"], "\"test string\"")

  def test_single_quotes_inner (self):
    result = expand_region_handler.expand_to_quotes(self.string2, 6, 12);
    self.assertEqual(result["start"], 1)
    self.assertEqual(result["end"], 12)
    self.assertEqual(result["string"], "test string")

  def test_single_quotes_outer (self):
    result = expand_region_handler.expand_to_quotes(self.string2, 1, 12);
    self.assertEqual(result["start"], 0)
    self.assertEqual(result["end"], 13)
    self.assertEqual(result["string"], "'test string'")

class SymbolTest(unittest.TestCase):
  def setUp(self):
    with open ("test/symbol_01.txt", "r") as myfile:
      self.string1 = myfile.read()
    with open ("test/symbol_02.txt", "r") as myfile:
      self.string2 = myfile.read()

  def test_symbol_inner (self):
    result = expand_region_handler.expand_to_symbols(self.string1, 7, 10);
    self.assertEqual(result["start"], 1)
    self.assertEqual(result["end"], 10)
    self.assertEqual(result["string"], "foo - bar")

  def test_symbol_outer (self):
    result = expand_region_handler.expand_to_symbols(self.string1, 1, 10);
    self.assertEqual(result["start"], 0)
    self.assertEqual(result["end"], 11)
    self.assertEqual(result["string"], "(foo - bar)")

  def test_look_back_dont_hang (self):
    result = expand_region_handler.expand_to_symbols("   ", 1, 2);
    self.assertEqual(result, None)

  def test_look_ahead_dont_hang (self):
    result = expand_region_handler.expand_to_symbols("(   ", 2, 2);
    self.assertEqual(result, None)

  def test_fix_look_back (self):
    result = expand_region_handler.expand_to_symbols(self.string2, 32, 32);
    self.assertEqual(result["start"], 12)
    self.assertEqual(result["end"], 35)
    self.assertEqual(result["string"], "foo.indexOf('bar') > -1")

class IntegrationTest(unittest.TestCase):
  def setUp(self):
    with open ("test/integration_01.txt", "r") as myfile:
      self.string1 = myfile.read()
    with open ("test/integration_02.txt", "r") as myfile:
      self.string2 = myfile.read()

  def test_word (self):
    result = expand_region_handler.expand(self.string1, 7, 7);
    self.assertEqual(result["start"], 6)
    self.assertEqual(result["end"], 9)
    self.assertEqual(result["string"], "bar")
    self.assertEqual(result["type"], "word")
    self.assertEqual(result["expand_stack"], ["word"])

  def test_quotes_inner (self):
    result = expand_region_handler.expand(self.string1, 6, 9);
    self.assertEqual(result["start"], 2)
    self.assertEqual(result["end"], 9)
    self.assertEqual(result["string"], "foo bar")
    self.assertEqual(result["type"], "quotes")
    self.assertEqual(result["expand_stack"], ["word", "quotes"])

  def test_quotes_outer (self):
    result = expand_region_handler.expand(self.string1, 2, 9);
    self.assertEqual(result["start"], 1)
    self.assertEqual(result["end"], 10)
    self.assertEqual(result["string"], "\"foo bar\"")
    self.assertEqual(result["type"], "quotes")
    self.assertEqual(result["expand_stack"], ["word", "quotes"])

  def test_symbol_inner (self):
    result = expand_region_handler.expand(self.string1, 1, 10);
    self.assertEqual(result["start"], 1)
    self.assertEqual(result["end"], 16)
    self.assertEqual(result["string"], "\"foo bar\" + \"x\"")
    self.assertEqual(result["type"], "symbol")
    self.assertEqual(result["expand_stack"], ["word", "quotes", "word_with_dots", "symbols"])

  def test_dont_expand_to_dots (self):
    result = expand_region_handler.expand(self.string2, 2, 5);
    self.assertEqual(result["start"], 1)
    self.assertEqual(result["end"], 10)
    self.assertEqual(result["string"], " foo.bar ")
    self.assertEqual(result["type"], "quotes")
    self.assertEqual(result["expand_stack"], ["word", "quotes"])

# def suite():
  # unittest.makeSuite(WordTest, "test")
  # unittest.makeSuite(QuoteTest, "test")
  # return unittest

if __name__ == "__main__":
  unittest.main()