import unittest
from pywiktionary.parsers import italian_parser


def get_pizza_html_extract():
    with open('../../file/html-responses/pizza-it.html', 'r', encoding='utf-8') as pizza_html_file:
        pizza_html = pizza_html_file.read()
    return pizza_html


def get_pizza_meanings_result():
    return {
        "noun": [
            {
                "meaning": "(gastronomia) focaccia di pasta composta principalmente da olio, mozzarella e pomodoro o altri ingredienti, e cotta al forno",
                "examples": [
                    "la pizza \u00e8 il mio piatto preferito"
                ]
            },
            {
                "meaning": "(familiare) si dice di persona, o cosa, particolarmente noiosa",
                "examples": [
                    "questo film \u00e8 una pizza"
                ]
            },
            {
                "meaning": "(cinematografia) contenitore di forma circolare con all'interno un rotolo di pellicola",
                "examples": []
            },
            {
                "meaning": "(per estensione) la stessa pellicola",
                "examples": [
                    "questa \u00e8 la pizza di 2001 odissea nello spazio"
                ]
            },
            {
                "meaning": "(gergale) (romano) schiaffo",
                "examples": [
                    "durante il litigio mi ha dato due pizze"
                ]
            }
        ]
    }


def get_pizza_parse_result():
    return {
        "meanings": get_pizza_meanings_result()
    }


class ItalianParserTestCase(unittest.TestCase):
    def test_get_meanings(self):
        parser = italian_parser.ItalianParser(get_pizza_html_extract())
        self.assertDictEqual(parser.get_meanings(), get_pizza_meanings_result())

    def test_parsing(self):
        parser = italian_parser.ItalianParser(get_pizza_html_extract())
        self.assertDictEqual(parser.parse(), get_pizza_parse_result())


if __name__ == '__main__':
    unittest.main()
