import requests

import pywiktionary
import pywiktionary.parsers.basic_parser
import pywiktionary.parsers.english_parser
import pywiktionary.parsers.italian_parser


LANGUAGE_CODES = {
    'italian': 'it',
    'it': 'it',
    'english': 'en',
    'en': 'en'
}

LANGUAGE_PARSERS = {
    'it': pywiktionary.parsers.italian_parser.ItalianParser,
    'en': pywiktionary.parsers.english_parser.EnglishParser
}


class WiktionaryParser:
    def __init__(self, default_language='en', parser_class=None):
        self._base_url = 'https://{lang_code}.wiktionary.org/w/api.php?format=json&action=query&prop=extracts&titles={page_title}'
        self.default_language = LANGUAGE_CODES[default_language] if default_language in LANGUAGE_CODES else 'en'
        if parser_class:
            self.parser_class = parser_class
        else:
            if self.default_language in LANGUAGE_PARSERS:
                self.parser_class = LANGUAGE_PARSERS[self.default_language]
            else:
                self.parser_class = pywiktionary.parsers.basic_parser.BasicParser

    def get_page(self, title, language=None):
        if not language or language not in LANGUAGE_CODES:
            language = self.default_language
        return self.parser_class(requests.get(self._format_url(title, language)).json())

    def _format_url(self, title, language):
        return self._base_url.format(lang_code=language, page_title=title)
