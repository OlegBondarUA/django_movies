from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from queue import Queue

from requests import Session
from bs4 import BeautifulSoup


class ScrapeMoviLinks:
    LOCK = Lock()
    TIME = 10

    def __init__(self, domain_url: str, last_page: int):
        self._domain_url = domain_url
        self._last_page = last_page

    def scrape(self):
        qu = self._fill_queue()
        print('Start scrapping!')
        with ThreadPoolExecutor(max_workers=5) as executor:
            for i in range(self._last_page):
                executor.submit(self._scrape, qu)

    def _fill_queue(self):
        qu = Queue()
        for number_page in range(1, self._last_page + 1):
            qu.put(self._domain_url.format(number_page=number_page))

        return qu

    def _scrape(self, qu: Queue):
        while True:
            url = qu.get()
            print(qu.qsize(), url)
            try:
                response_string = self._get_response(url)
                self._process(response_string)
            except Exception as error:
                print('Error', error)
                qu.put(url)

            if qu.empty():
                break

    def _get_response(self, url: str) -> str:
        try:
            with Session() as session:
                response = session.get(url, timeout=self.TIME)
                print(response.status_code)
                assert response.status_code == 200, 'Bad response'
            return response.text

        except Exception as error:
            print(error)

    def _process(self, html_string: str):
        soup = BeautifulSoup(html_string, 'html.parser')
        movies = soup.find_all('a', class_="poster-item")
        movies_link = []
        with self.LOCK:
            for links in movies:
                link = links.get('href').strip()
                movies_link.append(link)

        with open('links.txt', 'a') as file:
            for line in movies_link:
                file.write(line + '\n')


def main():
    domain = 'https://ilovekino.online/f/cat=2/r.imdb_rating=5;10/' \
             'r.kinopoisk_rating=6;10/r.year=2010;2022/sort=rating/' \
             'order=desc/page/{number_page}'
    last_page = 74

    scraper = ScrapeMoviLinks(domain, last_page)
    scraper.scrape()


if __name__ == '__main__':
    main()
