class BasicParser:
    def __init__(self, wiktionary_json):
        self.wiktionary_json = wiktionary_json

    def parse(self):
        raise NotImplementedError()
