# PyWiktionary

The Python library for wiktionary words

## Version 0.1.0

This is an alpha library to retrieve and parse [Wiktionary](https://wiktionary.org) word pages that will require enhancements and fixes


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

Initialize the parser factory (_pywiktionary.wiktionary_parser_factory.**WiktionaryParserFactory**_) with a supported language, then make the request with get_page() method passing the word you desire to get.
```python
from pywiktionary.wiktionary_parser_factory import WiktionaryParserFactory

parser_factory = WiktionaryParserFactory(default_language='en')
pizza_parser = parser_factory.get_page('pizza')
```

Then to get data about the word use the **parse()** method of the parser object returned from WiktionaryParserFactory:
```python
parsing_result = pizza_parser.parse()
```

The result variable is a dictionary containing the result of the wiktionary page parsing divided by type/subtype. Here the result for "pizza":
```
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
pizza_parser = parser_factory.get_page('pizza')
parsing_result = pizza_parser.parse()
```

Yeah, yeah... i know it is beautiful and easy as idea, but this library require many development to enhance this system!


### Supported languages (Language - Code)
 - English - en
 - Italian - it
 
## ToDo

 - Surfable Software Documentation!
 - Implement a good system to select wiktionary language parser
 - Write a good human friend documentation! =)
 - Write some examples for humans!