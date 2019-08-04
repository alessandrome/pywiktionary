from . import basic_parser
from bs4 import BeautifulSoup

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
        if not self.wiktionary_json:
            raise ValueError()
        words = {}
        page_list = list(self.wiktionary_json['query']['pages'].values())
        for page in page_list:
            word = {}
            soup = BeautifulSoup(page['extract'], 'html.parser')
            language_section = ""
            language_tag = soup.find(id='Italiano')
            if language_tag:
                for el in soup.find(id='Italiano').parent.next_siblings:
                    if el.name == 'h2':
                        soup = BeautifulSoup(language_section, 'html.parser')
                        break
                    language_section += str(el)
                word['meanings'] = self.get_meanings(soup)
                words[page['title']] = word
        return words

    def get_meanings(self, soup, meaning_types=list(SECTION_ID.keys()), get_examples=True, get_empty_meaning_types=False):
        meanings = {}
        for meaning_type in meaning_types:
            if meaning_type in SECTION_ID:
                meaning_list = []
                title = soup.find(id=SECTION_ID[meaning_type])
                if title:
                    for li_meaning in title.find_next('ol').find_all('li'):
                        examples = []
                        example_list = li_meaning.find('ul')
                        if example_list:
                            example_list = example_list.extract()
                        if example_list and get_examples:
                            for li_example in example_list.find_all('li'):
                                examples.append(li_example.text)
                        meaning_list.append({
                            'meaning': li_meaning.text.rstrip(),
                            'examples': examples
                        })
                if get_empty_meaning_types or meaning_list:
                    meanings[meaning_type] = meaning_list
        return meanings
