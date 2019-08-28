import unittest
from unittest import mock
from pywiktionary.wiktionary_parser_factory import WiktionaryParserFactory
from pywiktionary.wiktionary_parser_factory import PageNotFoundException
from pywiktionary.parsers import basic_parser
from pywiktionary.parsers import english_parser
from requests.exceptions import RequestException


class CustomParser(basic_parser.BasicParser):
    def parse(self):
        return {'meanings': {}}


# This method will be used by the mock to replace requests.get
def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'https://en.wiktionary.org/w/index.php?printable=yes&title=pizza':
        return MockResponse(mocked_pizza_response(), 200)
    elif args[0] == 'https://en.wiktionary.org/w/index.php?printable=yes&title=page_not_found':
        return MockResponse(mocked_page_not_found_response(), 404)
    raise RequestException()


def mocked_pizza_response():
    with open('tests/file/html-responses/404-en.html', 'r', encoding='utf-8') as pizza_html_file:
        pizza_html = pizza_html_file.read()
    return pizza_html


def mocked_page_not_found_response():
    with open('tests/file/html-responses/404-en.html', 'r', encoding='utf-8') as not_found_html_file:
        not_found_html = not_found_html_file.read()
    return not_found_html


class WiktionaryParserFactoryTestCase(unittest.TestCase):
    def test_default_wiktionary_parser_factory(self):
        parser_factory = WiktionaryParserFactory()
        self.assertEqual(parser_factory.default_language, 'en')
        self.assertEqual(parser_factory.default_parser_class, english_parser.EnglishParser)

    def test_custom_parser_class_parser_factory(self):
        parser_factory = WiktionaryParserFactory(default_parser_class=CustomParser)
        self.assertEqual(parser_factory.default_parser_class, CustomParser)

    def test_default_parser_class_parser_factory_on_unimplemented_language(self):
        parser_factory = WiktionaryParserFactory(default_language='falselanguage')
        self.assertEqual(parser_factory.default_language, 'falselanguage')
        self.assertEqual(parser_factory.default_parser_class, basic_parser.BasicParser)
        parser_factory = WiktionaryParserFactory(default_language='falselanguage', default_parser_class=CustomParser)
        self.assertEqual(parser_factory.default_language, 'falselanguage')
        self.assertEqual(parser_factory.default_parser_class, CustomParser)

    def test_url_format(self):
        parser_factory = WiktionaryParserFactory()
        formatted = parser_factory._format_url('en', 'page_title')
        self.assertEqual(formatted, 'https://en.wiktionary.org/w/index.php?printable=yes&title=page_title')

    # We patch 'requests.get' with our own method. The mock object is passed in to our test case method.
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_request_success(self, magic_mock):
        parser_factory = WiktionaryParserFactory('en')
        result = parser_factory.get_page('pizza')
        self.assertIsInstance(result, english_parser.EnglishParser)
        self.assertEqual(result.html, mocked_pizza_response())

    # We patch 'requests.get' with our own method. The mock object is passed in to our test case method.
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_request_page_not_found(self, magic_mock):
        parser_factory = WiktionaryParserFactory('en')
        result = parser_factory.get_page('page_not_found')
        expected_result = mocked_page_not_found_response()
        self.assertRaises(PageNotFoundException, parser_factory.get_page, 'page_not_found')


if __name__ == '__main__':
    unittest.main()
