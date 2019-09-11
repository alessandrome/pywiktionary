from . import basic_parser
from bs4 import BeautifulSoup
import copy
import re


SECTION_ID = {
    'noun': 'Sostantivo',
    'verb': 'Verbo',
    'adverb': 'Avverbio',
    'adjective': 'Aggettivo',
    'preposition': 'Preposizione',
    'numeral_ordinal': 'Ordinale',
    'numeral_cardinal': 'Cardinale',
    'proper_noun': 'Nome_proprio',
    'pronoun': 'Pronome',
    'particle': 'Particella',
    'interjection': 'Interiezione',
    'phrase': 'Frase',
    'contraction': 'Contrazione',
    'conjunction': 'Congiunzione',
    'article': 'Articolo',
    'suffix': 'Suffisso',
    'abbreviation': 'Acronimo_/_Abbreviazione',
    'chat_speaking': 'Abbreviazione_in_uso_nelle_chat',
    'proverb': 'Proverbio',
    'prefix': 'Prefisso'
}


class ItalianParser(basic_parser.BasicParser):
    def parse(self):
        if not self.html:
            raise ValueError()
        word = {'meanings': self.get_meanings()}
        return word

    def get_meanings(self, meaning_types=list(SECTION_ID.keys()), get_examples=True, get_empty_meaning_types=False):
        return self._get_meanings(self._get_language_soup('Italiano'), meaning_types, get_examples, get_empty_meaning_types)

    def _get_meanings(self, soup, meaning_types=list(SECTION_ID.keys()), get_examples=True, get_empty_meaning_types=False):
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
                            example_list = li_meaning.find('ul')
                            if example_list:
                                example_list = example_list.extract()
                                if get_examples:
                                    for li_example in example_list.find_all('li'):
                                        if li_example.text.rstrip():
                                            examples.append(re.sub(r'\s+', ' ', li_example.text).strip())
                            meaning_list.append({
                                'meaning': re.sub(r'\s+', ' ', li_meaning.text).strip(),
                                'examples': examples
                            })
                    if get_empty_meaning_types or meaning_list:
                        meanings[meaning_type] = meaning_list
        return meanings

    def _get_language_soup(self, language_section_id):
        language_tag = self.soup.find(id=language_section_id)
        if language_tag:
            italian_section_html = ''
            for el in self.soup.find(id=language_section_id).parent.next_siblings:
                if el.name == 'h2':
                    break
                italian_section_html += str(el)
            return BeautifulSoup(italian_section_html, 'html.parser')
        else:
            return None
