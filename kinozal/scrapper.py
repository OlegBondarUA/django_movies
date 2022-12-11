import logging
import sys
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from queue import Queue
from django.db.transaction import atomic

from translate import Translator
import requests
from bs4 import BeautifulSoup
from django.utils.text import slugify
from django.conf import settings

from kinozal.models import Category, Director, Actor, Film, Comment, Country


logger = logging.getLogger('logit')


class ScrapeMovies:
    TIME = 10
    LOCK = Lock()

    def __init__(self, list_url: list):
        self._list_url = list_url

    def scrape(self):
        qu = self._fill_queue()
        print('Started scrapping!')
        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.submit(self._scrape, qu)

    def _fill_queue(self):
        qu = Queue()

        for url in self._list_url:
            qu.put(url)

        return qu

    def _scrape(self, qu: Queue):
        while True:
            url = qu.get()
            print(qu.qsize(), url)
            try:
                response_string = self._get_response(url)
                self._process(response_string, url)
            except Exception as error:
                print('Error', error)
                qu.put(url)

            if qu.qsize() == 0:
                break

    def _get_response(self, url: str):
        try:
            with requests.Session() as session:
                response = session.get(url, timeout=self.TIME)
                print(response.status_code)
                assert response.status_code == 200, 'Bad response'
            return response.text

        except Exception as error:
            print(error)

    @atomic
    def _process(self, html_string: str, url):
        translator = Translator(from_lang="uk", to_lang="en")
        soup = BeautifulSoup(html_string, 'html.parser')
        with self.LOCK:
            try:
                title = soup.select(".page__header h1")
                title = title[0].text.strip().split('(')[0]
                title_slug = translator.translate(title).replace(' ', '-').lower()

                release_year = soup.select('.page__details ul li a')
                release_year = release_year[0].text.strip()

                country = soup.select('.page__details ul li span')
                country = country[1].text.strip().split(',')

                views = soup.select('.page__activity-item')
                views = views[0].text.strip()

                rating = soup.select('.page__rating-item')
                rating = rating[0].text.strip().split(' ')[1]

                description = soup.select('.page__text')
                description = description[0].text.strip()

                movie_link = soup.select('.tabs-block__content iframe')
                movie_link = movie_link[1].get('src')

                trailer_link = soup.select('.page__trailer iframe')
                trailer_link = trailer_link[0].get('src')

                comment = soup.select('.comment-item__main')
                comment = comment[0].text.strip() if comment else None

                category = soup.select('.page__meta-item')
                category = category[0].text.strip().split('/')

                directors = soup.select('.page__details-list li span')
                directors = directors[5].text.strip().split(',')

                actors = soup.select('.page__info-subinfo .line-clamp')
                actors = actors[0].text.strip().split(': ')[1:]
                actors = actors[0].split(',')

                image = soup.select('.page__poster img')
                image = f'https://ilovekino.online' \
                        f'{image[0].get("data-src").strip()}'

                image_name = image.split('-')[-1].split('/')[0].replace(' ',
                                                                        '-')
                self._upload_image_to_local_media(image, image_name)

                film, create = Film.objects.get_or_create(
                    defaults={
                        'base_url': url,
                        'title': title,
                        'image': f'images/{image_name}',
                        'release_year': release_year,
                        'views': views,
                        'rating': rating,
                        'description': description,
                        'movie_link': movie_link,
                        'trailer_link': trailer_link,
                    },
                    slug=slugify(title_slug := title_slug)
                )

                for item in country:
                    countries, _ = Country.objects.get_or_create(
                        country=item.strip())
                    film.country.add(countries)

                for categor in category:
                    category_slag = translator.translate(categor)
                    cat, create = Category.objects.get_or_create(
                        name=categor.strip(),
                        slug=slugify(category_slag := category_slag.strip().lower()))
                    film.categories.add(cat)

                for dire in directors:
                    direct, _ = Director.objects.get_or_create(name=dire)
                    film.directors.add(direct)

                for actor in actors:
                    act, _ = Actor.objects.get_or_create(name=actor)
                    film.actors.add(act)

                for comments in comment:
                    comm, _ = Comment.objects.get_or_create(comment=comments)
                    film.comments.add(comm)

            except Exception as error:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logger.error(f'Parser Error {error} {exc_tb.tb_lineno}')

    def _upload_image_to_local_media(self, img_url: str, image_name: str):
        with requests.Session() as session:
            img_response = session.get(img_url, timeout=self.TIME)

        with open(f'media/images/{image_name}', 'wb') as file:
            file.write(img_response.content)


def main():
    list_url = []
    with open(f'{settings.BASE_DIR}/kinozal/links.txt') as file:
        links = file.readlines()

    for url in links:
        list_url.append(url.strip())

    scraper = ScrapeMovies(list_url)
    scraper.scrape()


if __name__ == '__main__':
    main()
