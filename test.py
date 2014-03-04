import unittest

try:
  import expand_region_handler
except:
  from . import expand_region_handler

class LinebreaksTest(unittest.TestCase):
  def setUp(self):
    with open ("test/linebreak_01.txt", "r") as myfile:
      self.string1 = myfile.read()

  def test_find_linebreak (self):
    self.assertTrue(expand_region_handler.selection_contain_linebreaks(self.string1, 0, 8))

  def test_dont_find_linebreak (self):
    self.assertFalse(expand_region_handler.selection_contain_linebreaks("aaa", 1, 2))


class GetLineTest(unittest.TestCase):
  def setUp(self):
    with open ("test/line_01.txt", "r") as myfile:
      self.string1 = myfile.read()

  def test_get_line (self):
    result = expand_region_handler.get_line(self.string1, 13, 13);
    self.assertEqual(result["start"], 8)
    self.assertEqual(result["end"], 18)


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

  def test_existing_line_selection (self):
    result = expand_region_handler.expand_to_line(self.string1, 10, 18);
    self.assertEqual(result, None)

  def test_with_no_spaces_or_tabs_at_beginning (self):
    result = expand_region_handler.expand_to_line(self.string2, 6, 12);
    self.assertEqual(result["string"], "is it me")
    self.assertEqual(result["start"], 6)
    self.assertEqual(result["end"], 14)

  def test_with_indention (self):
    result = expand_region_handler.expand_to_line(" aa", 0, 0);
    self.assertEqual(result["string"], " aa")
    self.assertEqual(result["start"], 0)
    self.assertEqual(result["end"], 3)

  def test_without_indention (self):
    result = expand_region_handler.expand_to_line(" aa", 1, 1);
    self.assertEqual(result["string"], "aa")
    self.assertEqual(result["start"], 1)
    self.assertEqual(result["end"], 3)

  def test_with_indention2 (self):
    result = expand_region_handler.expand_to_line("  aa", 1, 1);
    self.assertEqual(result["string"], "  aa")
    self.assertEqual(result["start"], 0)
    self.assertEqual(result["end"], 4)


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

  def test_should_not_find1 (self):
    result = expand_region_handler.expand_to_quotes(" ': '", 1, 1);
    self.assertEqual(result, None)

  def test_should_not_find2 (self):
    result = expand_region_handler.expand_to_quotes("': '", 4, 4);
    self.assertEqual(result, None)


class TrimTest(unittest.TestCase):
  def setUp(self):
    with open ("test/trim_01.txt", "r") as myfile:
      self.string1 = myfile.read()
    with open ("test/trim_02.txt", "r") as myfile:
      self.string2 = myfile.read()

  def test_1 (self):
    result = expand_region_handler.trimSpacesAndTabsOnStartAndEnd("  aa  ");
    self.assertEqual(result["start"], 2)
    self.assertEqual(result["end"], 4)

  def test_2 (self):
    result = expand_region_handler.trimSpacesAndTabsOnStartAndEnd("  'a a'  ");
    self.assertEqual(result["start"], 2)
    self.assertEqual(result["end"], 7)

  def test_3 (self):
    result = expand_region_handler.trimSpacesAndTabsOnStartAndEnd(self.string1);
    self.assertEqual(result["start"], 2)
    self.assertEqual(result["end"], 11)

  def test_4 (self):
    result = expand_region_handler.trimSpacesAndTabsOnStartAndEnd(" foo.bar['property'].getX()");
    self.assertEqual(result["start"], 1)
    self.assertEqual(result["end"], 27)

  def test_5 (self):
    result = expand_region_handler.trimSpacesAndTabsOnStartAndEnd(self.string2);
    self.assertEqual(result["start"], 2)
    self.assertEqual(result["end"], 49)

class SemanticUnit(unittest.TestCase):
  def setUp(self):
    with open ("test/semantic_unit_01.txt", "r") as myfile:
      self.string1 = myfile.read()
    with open ("test/semantic_unit_02.txt", "r") as myfile:
      self.string2 = myfile.read()
    with open ("test/semantic_unit_03.txt", "r") as myfile:
      self.string3 = myfile.read()
    with open ("test/semantic_unit_04.txt", "r") as myfile:
      self.string4 = myfile.read()
    with open ("test/semantic_unit_05.txt", "r") as myfile:
      self.string5 = myfile.read()

  def test_1 (self):
    result = expand_region_handler.expand_to_semantic_unit(self.string1, 13, 13);
    self.assertEqual(result["string"], "foo.bar['property'].getX()")
    self.assertEqual(result["start"], 7)
    self.assertEqual(result["end"], 33)

  def test_2 (self):
    result = expand_region_handler.expand_to_semantic_unit(self.string2, 13, 13);
    self.assertEqual(result["string"], "foo.bar['prop,erty'].getX()")
    self.assertEqual(result["start"], 7)
    self.assertEqual(result["end"], 34)

  def test_3 (self):
    result = expand_region_handler.expand_to_semantic_unit(self.string3, 13, 13);
    self.assertEqual(result["string"], "foo.bar['property'].getX()")
    self.assertEqual(result["start"], 13)
    self.assertEqual(result["end"], 39)

  def test_4 (self):
    result = expand_region_handler.expand_to_semantic_unit(self.string4, 11, 11);
    self.assertEqual(result["start"], 7)
    self.assertEqual(result["end"], 51)

  def test_5 (self):
    result = expand_region_handler.expand_to_semantic_unit(self.string4, 6, 52);
    self.assertEqual(result["start"], 2)
    self.assertEqual(result["end"], 52)

  def test_6 (self):
    result = expand_region_handler.expand_to_semantic_unit(self.string5, 15, 15);
    self.assertEqual(result["string"], "o.getData(\"bar\")")
    self.assertEqual(result["start"], 8)
    self.assertEqual(result["end"], 24)

  def test_should_none (self):
    result = expand_region_handler.expand_to_semantic_unit("aaa", 1, 1);
    self.assertEqual(result, None)


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
    with open ("test/integration_03.txt", "r") as myfile:
      self.string3 = myfile.read()

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
    self.assertEqual(result["type"], "semantic_unit")
    self.assertEqual(result["expand_stack"], ["word", "quotes", "semantic_unit"])

  def test_dont_expand_to_dots (self):
    result = expand_region_handler.expand(self.string2, 2, 5);
    self.assertEqual(result["start"], 1)
    self.assertEqual(result["end"], 10)
    self.assertEqual(result["string"], " foo.bar ")
    self.assertEqual(result["type"], "quotes")
    self.assertEqual(result["expand_stack"], ["word", "quotes"])

  def test_expand_to_line (self):
    result = expand_region_handler.expand(self.string3, 30, 35);
    self.assertEqual(result["start"], 28)
    self.assertEqual(result["end"], 37)
    self.assertEqual(result["string"], "foo: true")
    self.assertEqual(result["type"], "line")
    self.assertEqual(result["expand_stack"], ["word", "quotes", "semantic_unit", "symbols", "line"])

  def test_expand_to_symbol_from_line (self):
    result = expand_region_handler.expand(self.string3, 28, 37);
    self.assertEqual(result["start"], 23)
    self.assertEqual(result["end"], 40)
    self.assertEqual(result["string"], "\n    foo: true\n  ")
    self.assertEqual(result["type"], "symbol")
    self.assertEqual(result["expand_stack"], ["semantic_unit", "symbols"])

  def test_skip_some_because_of_linebreak (self):
    result = expand_region_handler.expand(self.string3, 22, 41);
    self.assertEqual(result["start"], 15)
    self.assertEqual(result["end"], 41)
    self.assertEqual(result["string"], "return {\n    foo: true\n  }")
    self.assertEqual(result["type"], "semantic_unit")
    self.assertEqual(result["expand_stack"], ["semantic_unit"])

  def test_skip_some_because_of_linebreak_2 (self):
    result = expand_region_handler.expand(self.string3, 15, 41);
    self.assertEqual(result["start"], 12)
    self.assertEqual(result["end"], 42)
    self.assertEqual(result["type"], "symbol")
    self.assertEqual(result["expand_stack"], ["semantic_unit", "symbols"])

# def suite():
  # unittest.makeSuite(WordTest, "test")
  # unittest.makeSuite(QuoteTest, "test")
  # return unittest

if __name__ == "__main__":
  unittest.main()