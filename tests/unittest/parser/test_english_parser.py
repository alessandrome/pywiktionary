import unittest
from pywiktionary.parsers import italian_parser


def get_pizza_html_extract():
    with open('../../file/html-responses/pizza-en.html', 'r', encoding='utf-8') as pizza_html_file:
        pizza_html = pizza_html_file.read()
    return pizza_html


def get_pizza_meanings_result():
    return {
        "noun": [
            {
                "meaning": "(uncountable) A baked Italian dish of a thinly rolled bread dough crust typically topped "
                           "before baking with tomato sauce, cheese, and other ingredients such as meat, vegetables "
                           "or fruit",
                "examples": []
            },
            {
                "meaning": "(countable) A single instance of this dish",
                "examples": []
            }
        ]
    }


def get_pizza_parse_result():
    return {
        "meanings": get_pizza_meanings_result()
    }


class EnglishParserTestCase(unittest.TestCase):
    def test_get_meanings(self):
        parser = italian_parser.ItalianParser(get_pizza_html_extract())
        self.assertDictEqual(parser.get_meanings(), get_pizza_meanings_result())

    def test_parsing(self):
        parser = italian_parser.ItalianParser(get_pizza_html_extract())
        self.assertDictEqual(parser.parse(), get_pizza_parse_result())


if __name__ == '__main__':
    unittest.main()
