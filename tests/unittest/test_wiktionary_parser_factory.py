import unittest
from unittest import mock
from pywiktionary.wiktionary_parser_factory import WiktionaryParserFactory
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

    if args[0] == 'https://en.wiktionary.org/w/api.php?format=json&action=query&prop=extracts&titles=pizza':
        return MockResponse(mocked_pizza_json_response(), 200)
    elif args[0] == 'https://en.wiktionary.org/w/api.php?format=json&action=query&prop=extracts&titles=page_not_found':
        return MockResponse(mocked_page_not_found_json_response(), 200)
    raise RequestException()


def mocked_pizza_json_response():
    return {
        "batchcomplete": "",
        "warnings": {
            "extracts": {
                "*": "\"exlimit\" was too large for a whole article extracts request, lowered to 1.\nHTML may be malformed and/or unbalanced and may omit inline images. Use at your own risk. Known problems are listed at https://www.mediawiki.org/wiki/Extension:TextExtracts#Caveats."
            }
        },
        "query": {
            "pages": {
                "5801": {
                    "pageid": 5801,
                    "ns": 0,
                    "title": "pizza",
                    "extract": "<h2>This will not be extract in this unit test</h2>"
                }
            }
        }
    }


def mocked_page_not_found_json_response():
    return {
        "batchcomplete": "",
        "warnings": {
            "extracts": {
                "*": "\"exlimit\" was too large for a whole article extracts request, lowered to 1.\nHTML may be malformed and/or unbalanced and may omit inline images. Use at your own risk. Known problems are listed at https://www.mediawiki.org/wiki/Extension:TextExtracts#Caveats."
            }
        },
        "query": {
            "normalized": [
                {
                    "from": "page_not_found",
                    "to": "page not found"
                }
            ],
            "pages": {
                "-1": {
                    "ns": -1,
                    "title": "page note found",
                    "special": ""
                },
            }
        }
    }


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
        expected_json_result = mocked_pizza_json_response()
        self.assertEqual("response" in result, True)
        self.assertEqual("parsers" in result, True)
        self.assertDictEqual(result["response"], expected_json_result)
        self.assertEqual("pizza" in result["parsers"], True)

    # We patch 'requests.get' with our own method. The mock object is passed in to our test case method.
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_request_page_not_found(self, magic_mock):
        parser_factory = WiktionaryParserFactory('en')
        result = parser_factory.get_page('page_not_found')
        expected_json_result = mocked_page_not_found_json_response()
        self.assertEqual("response" in result, True)
        self.assertEqual("parsers" in result, True)
        self.assertDictEqual(result["response"], expected_json_result)
        self.assertEqual("page not found" in result["parsers"], False)
        self.assertEqual(len(list(result["parsers"].values())), 0)


if __name__ == '__main__':
    unittest.main()
