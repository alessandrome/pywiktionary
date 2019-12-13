from bs4 import BeautifulSoup


class BasicParser:
    """Basic parser to be extended and implemented"""
    def __init__(self, html):
        """Init the HTML parser"""
        self.html = html
        self.soup = BeautifulSoup(html or '', 'html.parser')

    def parse(self):
        """Function that shuold implement the complete wiktionary page parsing"""
        raise NotImplementedError()
