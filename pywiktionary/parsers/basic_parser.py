from bs4 import BeautifulSoup


class BasicParser:
    def __init__(self, html):
        self.html = html
        self.soup = BeautifulSoup(html or '', 'html.parser')

    def parse(self):
        raise NotImplementedError()
