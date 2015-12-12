import unittest

from . import units_utils
from . import units_expand_to_word
from . import units_expand_to_word_with_dots
from . import units_expand_to_line
from . import units_expand_to_quotes
from . import units_expand_to_semantic_unit
from . import units_expand_to_symbol
from . import units_xml_helper
from . import integration_javascript
from . import integration_html
from . import integration_latex
from . import integration_python

if __name__ == "__main__":
  test_loader = unittest.TestLoader()
  suite = unittest.TestSuite()

  suite.addTests(test_loader.loadTestsFromTestCase(units_utils.UtilsTest))
  suite.addTests(test_loader.loadTestsFromTestCase(units_utils.GetLineTest))
  suite.addTests(test_loader.loadTestsFromTestCase(units_utils.TrimTest))

  suite.addTests(test_loader.loadTestsFromTestCase(units_expand_to_word.WordTest))
  suite.addTests(test_loader.loadTestsFromTestCase(units_expand_to_word_with_dots.WordWithDotsTest))
  suite.addTests(test_loader.loadTestsFromTestCase(units_expand_to_line.ExpandToLineTest))
  suite.addTests(test_loader.loadTestsFromTestCase(units_expand_to_quotes.ExpandToQuotesTest))
  suite.addTests(test_loader.loadTestsFromTestCase(units_expand_to_semantic_unit.ExpandToSemanticUnitTest))
  suite.addTests(test_loader.loadTestsFromTestCase(units_expand_to_symbol.ExpandToSymbolTest))
  suite.addTests(test_loader.loadTestsFromTestCase(units_xml_helper.XmlHelperTest))

  suite.addTests(test_loader.loadTestsFromTestCase(integration_javascript.JavascriptIntegrationTest))
  suite.addTests(test_loader.loadTestsFromTestCase(integration_html.HtmlIntegrationTest))
  suite.addTests(test_loader.loadTestsFromTestCase(integration_latex.LatexIntegrationTest))
  suite.addTests(test_loader.loadTestsFromTestCase(integration_python.PythonIntegrationTest))

  unittest.TextTestRunner(verbosity=2).run(suite)
