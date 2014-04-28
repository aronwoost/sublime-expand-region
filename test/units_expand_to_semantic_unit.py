import unittest

from expand_to_semantic_unit import *

class ExpandToSemanticUnitTest(unittest.TestCase):

  @classmethod
  def setUpClass(self):
    with open ("test/snippets/semantic_unit_01.txt", "r") as myfile:
      self.string1 = myfile.read()
    with open ("test/snippets/semantic_unit_02.txt", "r") as myfile:
      self.string2 = myfile.read()
    with open ("test/snippets/semantic_unit_03.txt", "r") as myfile:
      self.string3 = myfile.read()
    with open ("test/snippets/semantic_unit_04.txt", "r") as myfile:
      self.string4 = myfile.read()
    with open ("test/snippets/semantic_unit_05.txt", "r") as myfile:
      self.string5 = myfile.read()
    with open ("test/snippets/semantic_unit_06.txt", "r") as myfile:
      self.string6 = myfile.read()
    with open ("test/snippets/semantic_unit_07.txt", "r") as myfile:
      self.string7 = myfile.read()
    with open ("test/snippets/semantic_unit_08.txt", "r") as myfile:
      self.string8 = myfile.read()
    with open ("test/snippets/semantic_unit_09.txt", "r") as myfile:
      self.string9 = myfile.read()

  def test_1 (self):
    result = expand_to_semantic_unit(self.string1, 13, 13);
    self.assertEqual(result["string"], "foo.bar['property'].getX()")
    self.assertEqual(result["start"], 7)
    self.assertEqual(result["end"], 33)

  def test_2 (self):
    result = expand_to_semantic_unit(self.string2, 13, 13);
    self.assertEqual(result["string"], "foo.bar['prop,erty'].getX()")
    self.assertEqual(result["start"], 7)
    self.assertEqual(result["end"], 34)

  def test_3 (self):
    result = expand_to_semantic_unit(self.string3, 13, 13);
    self.assertEqual(result["string"], "foo.bar['property'].getX()")
    self.assertEqual(result["start"], 13)
    self.assertEqual(result["end"], 39)

  def test_4 (self):
    result = expand_to_semantic_unit(self.string4, 11, 11);
    self.assertEqual(result["start"], 7)
    self.assertEqual(result["end"], 51)

  def test_5 (self):
    result = expand_to_semantic_unit(self.string4, 6, 52);
    self.assertEqual(result["start"], 2)
    self.assertEqual(result["end"], 52)

  def test_6 (self):
    result = expand_to_semantic_unit(self.string5, 15, 15);
    self.assertEqual(result["string"], "o.getData(\"bar\")")
    self.assertEqual(result["start"], 8)
    self.assertEqual(result["end"], 24)

  def test_7 (self):
    result = expand_to_semantic_unit("if (foo.get('a') && bar.get('b')) {", 6, 6);
    self.assertEqual(result["string"], "foo.get('a')")
    self.assertEqual(result["start"], 4)
    self.assertEqual(result["end"], 16)

  def test_8 (self):
    result = expand_to_semantic_unit("if (foo.get('a') || bar.get('b')) {", 6, 6);
    self.assertEqual(result["string"], "foo.get('a')")
    self.assertEqual(result["start"], 4)
    self.assertEqual(result["end"], 16)

  def test_9 (self):
    result = expand_to_semantic_unit(self.string9, 0, 14);
    self.assertEqual(result["string"], "if(foo || bar) {\n}")
    self.assertEqual(result["start"], 0)
    self.assertEqual(result["end"], 18)

  def test_should_none (self):
    result = expand_to_semantic_unit("aaa", 1, 1);
    self.assertEqual(result, None)

  def test_should_none_2 (self):
    result = expand_to_semantic_unit(self.string6, 6, 23);
    self.assertEqual(result, None)

  def test_should_none_3 (self):
    result = expand_to_semantic_unit(self.string7, 17, 33);
    self.assertEqual(result, None)

  def test_should_none_4 (self):
    result = expand_to_semantic_unit(self.string8, 16, 16);
    self.assertEqual(result, None)

  def test_should_none_5 (self):
    result = expand_to_semantic_unit("aa || bb", 3, 3);
    self.assertEqual(result, None)

if __name__ == "__main__":
  unittest.main()