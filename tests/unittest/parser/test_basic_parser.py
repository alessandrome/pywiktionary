import unittest
from pywiktionary.parsers import basic_parser


def get_pizza_html_extract():
    with open('tests/file/html-responses/pizza-it.html', 'r', encoding='utf-8') as pizza_html_file:
        pizza_html = pizza_html_file.read()
    return pizza_html


class BasicParseTestCase(unittest.TestCase):
    def test_init(self):
        parser = basic_parser.BasicParser(get_pizza_html_extract())
        self.assertEqual(get_pizza_html_extract(), parser.html)

    def test_parse_method(self):
        parser = basic_parser.BasicParser(get_pizza_html_extract())
        self.assertRaises(NotImplementedError, parser.parse)


if __name__ == '__main__':
    unittest.main()
