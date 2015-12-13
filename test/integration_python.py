import unittest

from expand_region_handler import *


class PythonIntegrationTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        with open("test/snippets/python_01.txt", "r") as myfile:
            self.string1 = myfile.read()
        with open("test/snippets/python_02.txt", "r") as myfile:
            self.string2 = myfile.read()

    def test_expand_to_subword1(self):
        result = expand(self.string1, 208, 208, "python")
        self.assertEqual(result["start"], 206)
        self.assertEqual(result["end"], 209)

    def test_expand_to_word1(self):
        result = expand(self.string1, 206, 209, "python")
        self.assertEqual(result["start"], 206)
        self.assertEqual(result["end"], 213)

    def test_expand_to_parens1(self):
        result = expand(self.string1, 206, 213, "python")
        self.assertEqual(result["start"], 206)
        self.assertEqual(result["end"], 218)

    def test_expand_to_parens2(self):
        result = expand(self.string1, 206, 218, "python")
        self.assertEqual(result["start"], 205)
        self.assertEqual(result["end"], 219)

    def test_expand_to_semantic_unit1(self):
        result = expand(self.string1, 205, 219, "python")
        self.assertEqual(result["start"], 204)
        self.assertEqual(result["end"], 219)

    def test_expand_to_line1(self):
        result = expand(self.string1, 204, 219, "python")
        self.assertEqual(result["start"], 195)
        self.assertEqual(result["end"], 219)

    def test_expand_to_indent1(self):
        result = expand(self.string1, 195, 219, "python")
        self.assertEqual(result["start"], 183)
        self.assertEqual(result["end"], 237)

    def test_expand_to_indent2(self):
        result = expand(self.string1, 183, 237, "python")
        self.assertEqual(result["start"], 169)
        self.assertEqual(result["end"], 237)

    def test_expand_to_indent3(self):
        result = expand(self.string1, 169, 237, "python")
        self.assertEqual(result["start"], 90)
        self.assertEqual(result["end"], 259)

    def test_expand_to_indent4(self):
        result = expand(self.string1, 90, 259, "python")
        self.assertEqual(result["start"], 63)
        self.assertEqual(result["end"], 259)

    def test_expand_to_indent5(self):
        result = expand(self.string1, 63, 259, "python")
        self.assertEqual(result["start"], 63)
        self.assertEqual(result["end"], 292)

    def test_expand_to_indent6(self):
        result = expand(self.string1, 63, 292, "python")
        self.assertEqual(result["start"], 44)
        self.assertEqual(result["end"], 292)

    def test_expand_not_to_no_indent(self):
        result = expand(self.string1, 44, 292, "python")
        self.assertEqual(result, None)

    def test_expand_from_block_start1(self):
        result = expand(self.string1, 177, 182, "python")
        self.assertEqual(result["start"], 169)
        self.assertEqual(result["end"], 237)

    def test_expand_from_block_start2(self):
        result = expand(self.string1, 67, 89, "python")
        self.assertEqual(result["start"], 63)
        self.assertEqual(result["end"], 259)

    def test_expand_from_block_start3(self):
        result = expand(self.string1, 44, 62, "python")
        self.assertEqual(result["start"], 44)
        self.assertEqual(result["end"], 292)

    def test_expand_over_line_cont1(self):
        result = expand(self.string2, 16, 28, "python")
        self.assertEqual(result["start"], 12)
        self.assertEqual(result["end"], 81)

    def test_expand_from_block_start4(self):
        result = expand(self.string2, 12, 81, "python")
        self.assertEqual(result["start"], 12)
        self.assertEqual(result["end"], 116)

if __name__ == "__main__":
    unittest.main()
