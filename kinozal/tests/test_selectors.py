from django.contrib.auth import get_user_model
from django.test import TestCase

from kinozal.selectors import (
    random_films_selector,
    max_rating_selector,
    categories_selector,
    years_selector,
    films_category_selector,
    related_film_selector,
    related_director_selector
)
from kinozal.models import Category, Film


class TestSelectors(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(username='some_user')
        self.category1 = Category(name='comedy', slug='comedy-slug')
        self.category1.save()
        self.category2 = Category(name='action', slug='action-slug')
        self.category2.save()
        self.category3 = Category(name='melodrama', slug='melodrama-slug')
        self.category3.save()

        self.film = Film(title='avatar',
                         release_year= 2002,
                         image='/Users/olegbondar/Python/project_django/Beetroot_django/media/images/255798820.jpg',
                         views= 100,
                         rating= 9,
                         description="posting",
                         movie_link='https://www.youtube.com/watch?v=5PSNL1qE6VY',
                         trailer_link='https://www.youtube.com/watch?v=5PSNL1qE6VY',
                         slug='avatar-slug')
        self.film.save()
        self.film.categories.add(self.category2)

        self.film = Film(title='alone at home',
                         release_year=1992,
                         image='/Users/olegbondar/Python/project_django/Beetroot_django/media/images/15249323.jpg',
                         views=756,
                         rating=7,
                         description="posting",
                         movie_link='https://www.youtube.com/watch?v=5PSNL1qE6VY',
                         trailer_link='https://www.youtube.com/watch?v=5PSNL1qE6VY',
                         slug='alone-at-home-slug')
        self.film.save()
        self.film.categories.add(self.category1)

        self.film = Film(title='titanic',
                         release_year=2000,
                         image='/Users/olegbondar/Python/project_django/Beetroot_django/media/images/49150562.jpg',
                         views=567,
                         rating=9,
                         description="posting",
                         movie_link='https://www.youtube.com/watch?v=5PSNL1qE6VY',
                         trailer_link='https://www.youtube.com/watch?v=5PSNL1qE6VY',
                         slug='titanic-slug')
        self.film.save()
        self.film.categories.add(self.category3)

        self.film = Film(title='christmas',
                         release_year=2022,
                         image='/Users/olegbondar/Python/project_django/Beetroot_django/media/images/155435585.jpg',
                         views=367,
                         rating=8,
                         description="posting",
                         movie_link='https://www.youtube.com/watch?v=5PSNL1qE6VY',
                         trailer_link='https://www.youtube.com/watch?v=5PSNL1qE6VY',
                         slug='christmas-slug')
        self.film.save()
        self.film.categories.add(self.category1, self.category2, self.category3)

    def test_random_films_selector(self):
        films = random_films_selector(2)
        self.assertEqual(len(films), 2)