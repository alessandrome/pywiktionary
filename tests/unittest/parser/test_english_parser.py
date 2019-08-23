import unittest
from pywiktionary.parsers import english_parser


def get_pizza_it_html_extract():
    with open('tests/file/html-responses/pizza-it.html', 'r', encoding='utf-8') as pizza_html_file:
        pizza_html = pizza_html_file.read()
    return pizza_html


def get_pizza_en_html_extract():
    with open('tests/file/html-responses/pizza-en.html', 'r', encoding='utf-8') as pizza_html_file:
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


def get_empty_parse_result():
    return {"meanings": {}}


def get_pizza_parse_result():
    return {
        "meanings": get_pizza_meanings_result()
    }


class EnglishParserTestCase(unittest.TestCase):
    def test_get_meanings(self):
        parser = english_parser.EnglishParser(html=get_pizza_en_html_extract())
        self.assertDictEqual(parser.get_meanings(), get_pizza_meanings_result())

    def test_empty_html_parsing(self):
        parser = english_parser.EnglishParser(html=None)
        self.assertRaises(ValueError, parser.parse)

    def test_parsing(self):
        parser = english_parser.EnglishParser(html=get_pizza_en_html_extract())
        self.assertDictEqual(parser.parse(), get_pizza_parse_result())

    def test_parsing_different_language(self):
        parser = english_parser.EnglishParser(html=get_pizza_it_html_extract())
        self.assertDictEqual(parser.parse(), get_empty_parse_result())

    def test_return_empty_meaning_types(self):
        parser = english_parser.EnglishParser(html=get_pizza_en_html_extract())
        self.assertListEqual(list(parser.get_meanings(get_empty_meaning_types=True).keys()), list(english_parser.SECTION_ID.keys()))


if __name__ == '__main__':
    unittest.main()
