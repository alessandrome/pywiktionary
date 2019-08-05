# PyWiktionary - a Python library for wiktionary words

## Version 0.0.1 (pre-alpha)

This is just a pre alpha that need so many enhancements and fixes, but could be a starting base to start a simple python library for [Wiktionary](https://.wiktionary.org) words

## Install

### Requirements

Before install, please, make sure you've installed the project dependencies if you're installing from source code:
```
$ pip install -r ./requirements.txt
```

### Pywiktionary install

Install from the source code:
```
$ pip install .
```

## How to use

First of all initialize the wiki parser with a supported language then make the request and at the end call the parse() method of the parser object returned from WiktionaryParser :
```python
from pywiktionary import WiktionaryParser

wiktionary_parser = WiktionaryParser(default_language='en')
language_parser = wiktionary_parser.get_page('pizza')
result = language_parser.parse()
```

The result variable is dictionary containing the result of the wiktionary page parsing. Here the result for "pizza":
```json
{
  "pizza": {
    "meanings": {
      "noun": [
        {
          "meaning": "(uncountable) A baked Italian dish of a thinly rolled bread dough crust typically topped before baking with tomato sauce, cheese, and other ingredients such as meat, vegetables or fruit",
          "examples": []
        },
        {
          "meaning": "(countable) A single instance of this dish",
          "examples": []
        }
      ]
    }
  }
}
```

Yeah, yeah... i know it is beautiful and easy as idea, but it now require some development to enhance this system!
### Supported languages
 - English - en
 - Italian - it
 
## ToDo

 - Implement a good system to select wiktionary language parser
 - Write a good human friend documentation! =)