import unittest
from queue import Queue
from unittest.mock import patch, call
from unittest.mock import MagicMock

from kinozal.scrapper import ScrapeMovies

class TestScrapeMovies(unittest.TestCase):
    def setUp(self):
        self.scraper = ScrapeMovies(['url1', 'url2'])
        self.html_string = '<html>...</html>'
        self.url = 'http://example.com'

    @patch.object(ScrapeMovies, '_extract_data_from_soup')
    @patch.object(ScrapeMovies, '_save_data_to_db')
    def test_process_success(self, mock_save, mock_extract):
        self.scraper._process(self.html_string, self.url)
        # mock_extract.assert_called_once_with(self.html_string, self.url)
        mock_save.assert_called_once_with(mock_extract.return_value)

    @patch('requests.Session.get')
    def test_scrape_success(self, mock_get):

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html>...</html>'
        mock_get.return_value = mock_response
        self.scraper._scrape(self.scraper._fill_queue())
        mock_get.assert_has_calls([call('url1', timeout=10), call('url2', timeout=10)])


    def test_fill_queue(self):
        qu = self.scraper._fill_queue()
        self.assertEqual(qu.qsize(), 2)
        self.assertEqual(qu.get(), 'url1')
        self.assertEqual(qu.get(), 'url2')
        self.assertEqual(qu.qsize(), 0)

    @patch('kinozal.scrapper.ScrapeMovies._fill_queue')
    @patch('kinozal.scrapper.ScrapeMovies._get_response')
    @patch('kinozal.scrapper.ScrapeMovies._process')
    def test__scrape(self, mock_process, mock_get_response, mock_fill_queue):
        mock_get_response.return_value = self.html_string
        mock_fill_queue.return_value = MagicMock(Queue)
        mock_fill_queue.return_value.get.side_effect = ['url1', 'url2']
        mock_fill_queue.return_value.qsize.return_value = 0
        scraper = ScrapeMovies(['url1', 'url2'])
        scraper.scrape()
        mock_get_response.assert_has_calls([call('url1'), call('url2')])
        self.assertEqual(mock_get_response.call_count, 2)
        mock_process.assert_has_calls([call('<html>...</html>', 'url1'), call('<html>...</html>', 'url2')])
        self.assertEqual(mock_process.call_count, 2)
        mock_fill_queue.assert_called_once()
        mock_fill_queue.return_value.get.assert_has_calls([call(), call()])
        self.assertEqual(mock_fill_queue.return_value.get.call_count, 10)
        self.assertEqual(mock_fill_queue.return_value.qsize.call_count, 4)

    @patch('kinozal.scrapper.ScrapeMovies._get_response')
    def test_scrape_error(self, mock_get_response):
        mock_get_response.side_effect = Exception('Error')
        scraper = ScrapeMovies(['url1', 'url2'])
        scraper._scrape(scraper._fill_queue())
        mock_get_response.assert_has_calls([call('url1'), call('url2')])
        self.assertEqual(mock_get_response.call_count, 2)