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


class WiktionaryParserFactory:
    def __init__(self, default_language='en', default_parser_class=None):
        # TODO: Raise an exception when a language not implemented yet has been passed AND the default parser class is not passed
        self._base_url = 'https://{lang_code}.wiktionary.org/w/index.php?printable=yes&title={page_title}'
        self.default_language = LANGUAGE_CODES[default_language] if default_language in LANGUAGE_CODES else default_language
        if default_parser_class:
            self.default_parser_class = default_parser_class
        else:
            if self.default_language in LANGUAGE_PARSERS:
                self.default_parser_class = LANGUAGE_PARSERS[self.default_language]
            else:
                self.default_parser_class = pywiktionary.parsers.basic_parser.BasicParser

    def get_page(self, title, language=None):
        if not language or language not in LANGUAGE_CODES:
            language = self.default_language
        wiktionary_response = requests.get(self._format_url(language=language, title=title))
        if wiktionary_response.status_code == 404:
            raise PageNotFoundException
        return self.default_parser_class(wiktionary_response.text)

    def _format_url(self, language, title):
        return self._base_url.format(lang_code=language, page_title=title)


class PageNotFoundException(requests.RequestException):
    pass
