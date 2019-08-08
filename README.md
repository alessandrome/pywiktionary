# PyWiktionary

The Python library for wiktionary words

## Version 0.0.2 (pre-alpha)

This is just a pre alpha that need so many enhancements and fixes, but could be a starting base to start a simple python library for [Wiktionary](https://wiktionary.org) words


## Install

### Requirements

If you install this library from source code or you want help with development of the code, make sure to install requirements first:
```
$ pip install -r ./requirements.txt
```

### Pywiktionary install

Install from the remote pip repository:
```
$ pip install pywiktionary
```

Install from the root of the source code:
```
$ pip install .
```


## How to use

First of all initialize the wiki parser factory (_pywiktionary.wiktionary_parser_factory.**WiktionaryParserFactory**_) with a supported language, then make the request with get_page() method passing the word you desire to get.
If you need to retrieve more words at once, pass a list of words divided by the pipe symbol (**|**)
```python
from pywiktionary.wiktionary_parser_factory import WiktionaryParserFactory

parser_factory = WiktionaryParserFactory(default_language='en')
parser_factory_result = parser_factory.get_page('pizza')
```

Below how the factory result should be appear, where Wiktionary Example Response can be tested [here](https://en.wiktionary.org/wiki/Special:ApiSandbox#action=query&format=json&prop=extracts&titles=pizza):
```json
{
  "response": <original wiktionary JSON response>,
  "parsers": {
    "pizza": <ParserObject for word 'pizza'>
  }
}
```

Based on how factory result is composed, here how to retrieve the parser:
```python
pizza_parser = parser_factory_result['parsers']['pizza']
```

Then to get info about the word use the parse() method of the parser object returned from WiktionaryParserFactory:
```python
parsing_result = pizza_parser.parse()
```

The result variable is dictionary containing the result of the wiktionary page parsing. Here the result for "pizza":
```json
{
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
```

#### Summary

This is the summary of above commented code:
```python
from pywiktionary.wiktionary_parser_factory import WiktionaryParserFactory

parser_factory = WiktionaryParserFactory(default_language='en')
parser_factory_result = parser_factory.get_page('pizza')
pizza_parser = parser_factory_result['parsers']['pizza']
parsing_result = pizza_parser.parse()
```

Yeah, yeah... i know it is beautiful and easy as idea, but this library require many development to enhance this system!


### Supported languages
 - English - en
 - Italian - it
 
## ToDo

 - Implement a good system to select wiktionary language parser
 - Write a good human friend documentation! =)
 - Write some examples for humans!