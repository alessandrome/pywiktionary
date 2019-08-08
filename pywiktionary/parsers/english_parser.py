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
    def parse(self):
        if not self.html:
            raise ValueError()
        word = {'meanings': self.get_meanings()}
        return word

    def get_meanings(self, meaning_types=list(SECTION_ID.keys()), get_examples=True, get_empty_meaning_types=False):
        return self._get_meanings(self._get_language_soup('English'), meaning_types, get_examples,
                                  get_empty_meaning_types)

    def _get_meanings(self, soup, meaning_types=list(SECTION_ID.keys()), get_examples=True,
                      get_empty_meaning_types=False):
        meanings = {}
        for meaning_type in meaning_types:
            if meaning_type in SECTION_ID:
                meaning_list = []
                title = soup.find(id=SECTION_ID[meaning_type])
                if title:
                    for li_meaning in title.find_next('ol').find_all('li', recursive=False):
                        examples = []
                        example_list = li_meaning.find('ul')
                        if example_list:
                            example_list = example_list.extract()
                            if get_examples:
                                for li_example in example_list.find_all('li'):
                                    if li_example.text.rstrip():
                                        examples.append(li_example.text.rstrip())
                        meaning_list.append({
                            'meaning': li_meaning.text.rstrip(),
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
