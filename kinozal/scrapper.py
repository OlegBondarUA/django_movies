import sys
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from django.db.transaction import atomic

import cyrtranslit
import requests
from bs4 import BeautifulSoup
from django.utils.text import slugify

from kinozal.models import Category, Director, Actor, Film, Comment


TIME_OUT = 10


def upload_image_to_local_media(
        img_url: str,
        image_name: str,
):
    with requests.Session() as session:
        img_response = session.get(img_url, timeout=TIME_OUT)

    with open(f'media/images/{image_name}', 'wb') as file:
        file.write(img_response.content)




@atomic
def process(html_string: str, url: str):
    soup = BeautifulSoup(html_string, 'html.parser')

    try:
        title = soup.select(".allhead .solototle")
        title = title[0].text.strip()

        release_year = soup.select(".fi-item .fi-desc")
        release_year = release_year[1].text.strip()

        country = soup.select(".fi-item .fi-desc")
        country = country[2].text.strip()

        duration = soup.select(".fi-item")
        if duration[6].text.strip().startswith('Тривалість:'):
            duration = duration[6].text.strip()
        else:
            duration = duration[7].text.strip()

        rating = soup.select(".fi-item")
        if rating[9].text.strip().startswith('Доступно на:'):
            rating = rating[8].text.strip()[0:3]
        else:
            rating = rating[9].text.strip()[0:3]
        print('RATING', rating)
        description = soup.find('div', class_="full-text clearfix")
        description = description.text.strip()

        image = soup.select(".film-poster a")
        for img in image:
            if img.get('href').startswith('https'):
                image = img.get('href')
            else:
                image = f'https://uakino.club{img.get("href")}'

        movie_link = soup.select('#pre')
        movie_link = [movie.get('src') for movie in movie_link]

        trailer_link = soup.select('#pre')
        trailer_link = [trailer.get('data-src') for trailer in trailer_link]
        for urls in trailer_link:
            trailer_link = urls

        film, create = Film.objects.get_or_create(
            defaults={
                'base_url': url,
                'title': title,
                'release_year': release_year,
                'country': country,
                'duration': duration,
                'rating': rating,
                'description': description,
                'image': image,
                'movie_link': movie_link[0],
                'trailer_link': trailer_link,
            },
            slug=slugify(title := cyrtranslit.to_latin(title.strip().lower()),
                         'me')
        )

        category = soup.select(".fi-item .fi-desc")
        category = category[3].text.strip().split(',')
        for categor in category:
            cat, create = Category.objects.get_or_create(name=categor.strip(),
                                                slug=categor.strip().lower())

            film.categories.add(cat)

        directors = soup.select(".fi-item .fi-desc")
        directors = directors[4].text.strip().split(',')
        for dire in directors:
            direct, _ = Director.objects.get_or_create(name=dire)

            film.directors.add(direct)

        actors = soup.select(".fi-item .fi-desc")
        actors = actors[5].text.strip().split(',')

        for actor in actors:
            act, _ = Actor.objects.get_or_create(name=actor)

            film.actors.add(act)

        comments = soup.select(".comments-tree-list .comm-body .comm-text")
        comments = [comment.text.strip() for comment in comments]

        for comment in comments:
            comm, _ = Comment.objects.get_or_create(comment=comment)

            film.comments.add(comm)

        image_name = title.split('/')[-1].split('/')[0].replace(' ', '-') + '.jpg'
        print('Uploading images')

        upload_image_to_local_media(
            image,
            image_name.lower(),
        )

        print('Done')

    except Exception as error:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print('Parsing Error', error, exc_tb.tb_lineno)


def worker(queue: Queue):
    while True:
        url = queue.get()
        print('[Working ON]', url)
        try:
            with requests.Session() as session:
                response = session.get(
                    url,
                    allow_redirects=True,
                    timeout=TIME_OUT
                )
                print(response.status_code)

                if response.status_code == 404:
                    print('Page not found', url)
                    break

                assert response.status_code in (200, 301, 302), 'Bad response'

            process(response.text, url)

        except (
            requests.Timeout,
            requests.TooManyRedirects,
            requests.ConnectionError,
            requests.RequestException,
            requests.ConnectionError,
            AssertionError
        ) as error:
            print('An error happen', error)
            queue.put(url)

        if queue.qsize() == 0:
            break


def main():
    film_url = 'https://uakino.club/filmy/page/1/'

    with requests.Session() as links_session:
        response = links_session.get(film_url)

    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.find_all('div', class_="movie-item short-item")
    links = [urls.find('a', class_="movie-title").get('href').strip()
             for urls in links]

    queue = Queue()

    for url in links:
        queue.put(url)

    worker_number = 20

    with ThreadPoolExecutor(max_workers=worker_number) as executor:
        for _ in range(worker_number):
            executor.submit(worker, queue)


if __name__ == '__main__':
    main()
