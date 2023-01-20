import unittest
from unittest.mock import patch, mock_open
from bs4 import BeautifulSoup

from kinozal.links_scrapper import ScrapeMoviLinks


class TestScrapeMoviLinks(unittest.TestCase):
    def setUp(self):
        self.domain = 'https://ilovekino.online/f/cat=2/r.imdb_rating=5;10/' \
             'r.kinopoisk_rating=6;10/r.year=2010;2022/sort=rating/' \
             'order=desc/page/{number_page}'
        self.last_page = 3
        self.scraper = ScrapeMoviLinks(self.domain, self.last_page)

    @patch('requests.Session.get')
    def test_get_response(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = '<html>...</html>'
        response_string = self.scraper._get_response(self.domain.format(number_page=1))
        self.assertEqual(response_string, '<html>...</html>')
        mock_get.assert_called_with(self.domain.format(number_page=1), timeout=10)

    def test_fill_queue(self):
        qu = self.scraper._fill_queue()
        self.assertEqual(qu.qsize(), self.last_page)
        self.assertEqual(qu.get(), self.domain.format(number_page=1))
        self.assertEqual(qu.get(), self.domain.format(number_page=2))
        self.assertEqual(qu.get(), self.domain.format(number_page=3))

    @patch('builtins.open', mock_open(read_data='<html>...</html>'))
    def test_process(self):
        soup = BeautifulSoup('<html>...</html>', 'html.parser')
        movies = soup.find_all('a', class_="poster-item")
        movies_link = []
        for links in movies:
            link = links.get('href').strip()
            movies_link.append(link)

        self.scraper._process('<html>...</html>')
        handle = open('links.txt', 'r')
        content = handle.read()
        for line in movies_link:
            self.assertIn(line, content)

    def test_process_fail(self):
        with self.assertRaises(TypeError):
            self.scraper._process(12)

if __name__ == '__main__':
    unittest.main()
