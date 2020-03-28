import os

from pywiktionary import WiktionaryParserFactory
import json
from bs4 import BeautifulSoup


def serialize(obj):
    return obj.__dict__


lang = 'en'
wikt_parser = WiktionaryParserFactory(lang)

word = 'pizza'
result = wikt_parser.get_page(word)
# print(json.dumps(result, indent=2, default=serialize))
print()
print('='*200)
parser = result

print(json.dumps(parser.parse(), indent=2))
print('='*200)

soup = BeautifulSoup(parser.html, 'html.parser')
print()
# print(soup.prettify())

try:
    # Create target Directory
    os.mkdir('word-examples')
except FileExistsError:
    pass
f = open('word-examples/{}-{}.html'.format(word, lang), 'w+', encoding='utf-8')
f.write(parser.html)
f.close()

print(json.dumps(parser.parse(), indent=2))
