import copy
import re

from . import basic_parser
from bs4 import BeautifulSoup

SECTION_ID = {
    'noun': 'Noun',
    'verb': 'Verb',
    'adverb': 'Adverb',
    'adjective': 'Adjective',
    'preposition': 'Preposition',
    'numeral': 'Numeral',
    'proper_noun': 'Proper_noun',
    'pronoun': 'Pronoun',
    'particle': 'Particle',
    'interjection': 'Interjection',
    'phrase': 'Phrase',
    'contraction': 'Contraction',
    'conjunction': 'Conjunction',
    'article': 'Article',
    'suffix': 'Suffix',
    'abbreviation': 'Abbreviation',
    'initialism': 'Initialism',
    'proverb': 'Proverb',
    'prefix': 'Prefix'
}


class EnglishParser(basic_parser.BasicParser):
    """Parser for english wiktionary pages"""
    def parse(self):
        """Parse the page to return word attributes. This is an extension of BasicParser

        :return: Word attributes. With first release this contain just the 'meaning' key
        :raises ValueError: Raise a ValueError exception if the parser has an empty invalid html
        """
        if not self.html:
            raise ValueError()
        word = {'meanings': self.get_meanings()}
        return word

    def get_meanings(self, get_examples=True, get_empty_meaning_types=False):
        return self._get_meanings(self._get_language_soup('English'), get_examples, get_empty_meaning_types)

    def _get_meanings(self, soup, get_examples=True, get_empty_meaning_types=False):
        meanings = {}
        if soup:
            soup_copy = copy.copy(soup)
            meaning_list_tags = soup_copy.find_all('ol')
            for ol_tag in meaning_list_tags:
                meaning_list = []
                type_tag = ol_tag.previous_element
                while type_tag and (not type_tag.name or (not type_tag.name.startswith('h') and not type_tag.name == 'p')):
                    type_tag = type_tag.previous_element
                if type_tag.name == 'p':
                    while type_tag and (not type_tag.name or not type_tag.name.startswith('h')):
                        type_tag = type_tag.previous_element
                    type_name = type_tag.get_text().lower()
                    for li_meaning in ol_tag.find_all('li', recursive=False):
                        examples = []
                        meaning_list.append({
                            'meaning':  re.sub(r'\s+', ' ', li_meaning.text).strip(),
                            'examples': examples
                        })
                    meanings[type_name] = meaning_list
        return meanings

    def get_meaning_by_list(self, meaning_types=list(SECTION_ID.keys()), get_examples=True, get_empty_meaning_types=False):
        """Get english meanings of the word find in the Wiktionary HTML page contained in this parser

        :param list meaning_types: List containing meaning type keys to looking for. By default this list contain all foundable keys
        :param boolean get_examples: Specify if the result should contain example of meanings. By default this is True
        :param boolean get_empty_meaning_types: Specify if empty meaning type keys should be included in the returned wiktionary. By default this is False
        :return dictionary: Return dictionary with all found meanings divided by meaning type keys. Each entry contain a list of dictionaries with two entry: 'meaning' which is a meaning of the word, and 'example' with a list of examples, if are present and should be returned, for the retrieved meaning.
        """
        return self._get_meanings_by_list(self._get_language_soup('English'), meaning_types, get_examples,
                                  get_empty_meaning_types)

    def _get_meaning_by_list(self, soup, meaning_types=list(SECTION_ID.keys()), get_examples=True, get_empty_meaning_types=False):
        """Private function for public get_meanings method that get the soup parser as input with the other passed parameters of get_meanings function"""
        meanings = {}
        if get_empty_meaning_types:
            for meaning_type in list(SECTION_ID.keys()):
                meanings[meaning_type] = []
        if soup:
            soup_copy = copy.copy(soup)
            for meaning_type in meaning_types:
                if meaning_type in SECTION_ID:
                    meaning_list = []
                    title = soup_copy.find(id=SECTION_ID[meaning_type])
                    if title:
                        for li_meaning in title.find_next('ol').find_all('li', recursive=False):
                            examples = []
                            example_list = li_meaning.find('dl')
                            if example_list:
                                example_list = example_list.extract()
                                if get_examples:
                                    for li_example in example_list.find_all('dd'):
                                        if li_example.text.rstrip():
                                            examples.append(re.sub(r'\s+', ' ', li_example.text).strip())
                            meaning_list.append({
                                'meaning':  re.sub(r'\s+', ' ', li_meaning.text).strip(),
                                'examples': examples
                            })
                    if get_empty_meaning_types or meaning_list:
                        meanings[meaning_type] = meaning_list
        return meanings

    def _get_language_soup(self, language_section_id):
        """Private function to get sub-soup parser just for the specified language looked for its code or id in the HTML wiktionary page"""
        language_tag = self.soup.find(id=language_section_id)
        if language_tag:
            english_section_html = ''
            for el in self.soup.find(id=language_section_id).parent.next_siblings:
                if el.name == 'h2':
                    break
                english_section_html += str(el)
            return BeautifulSoup(english_section_html, 'html.parser')
        else:
            return None
