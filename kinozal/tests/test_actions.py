from django.contrib.auth import get_user_model
from django.test import TestCase

from kinozal.actions import translate_film, translate_name
from kinozal.models import Category, Film, Director


class TestSelectors(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(username='some_user')
        self.category1 = Category(name='comedy', slug='comedy-slug')
        self.category1.save()
        self.category2 = Category(name='action', slug='action-slug')
        self.category2.save()
        self.category3 = Category(name='melodrama', slug='melodrama-slug')
        self.category3.save()

        self.director1 = Director(name='director1')
        self.director1.save()
        self.director2 = Director(name='director2')
        self.director2.save()
        self.director3 = Director(name='director3')
        self.director3.save()
        self.director4 = Director(name='director4')
        self.director4.save()


        self.film = Film(title='Аватар',
                         title_en='',
                         release_year= 2002,
                         image='/Users/olegbondar/Python/project_django/Beetroot_django/media/images/255798820.jpg',
                         views= 'переглядів 100',
                         rating= 9,
                         description="Описання фільму",
                         movie_link='https://www.youtube.com/watch?v=5PSNL1qE6VY',
                         trailer_link='https://www.youtube.com/watch?v=5PSNL1qE6VY',
                         slug='avatar-slug'
                         )

        self.film.save()
        self.film.categories.add(self.category2)
        self.film.directors.add(self.director1)

        self.film = Film(title='Один вдома',
                         title_en='',
                         release_year=1992,
                         image='/Users/olegbondar/Python/project_django/Beetroot_django/media/images/15249323.jpg',
                         views='переглядів 756',
                         rating=7,
                         description="Описання фільму",
                         movie_link='https://www.youtube.com/watch?v=5PSNL1qE6VY',
                         trailer_link='https://www.youtube.com/watch?v=5PSNL1qE6VY',
                         slug='alone-at-home-slug'
                         )
        self.film.save()
        self.film.categories.add(self.category1)
        self.film.directors.add(self.director2)

        self.film = Film(title='Титанік',
                         title_en='',
                         release_year=2000,
                         image='/Users/olegbondar/Python/project_django/Beetroot_django/media/images/49150562.jpg',
                         views='переглядів 567',
                         rating=6,
                         description="Описання фільму",
                         movie_link='https://www.youtube.com/watch?v=5PSNL1qE6VY',
                         trailer_link='https://www.youtube.com/watch?v=5PSNL1qE6VY',
                         slug='titanic-slug'
                         )
        self.film.save()
        self.film.categories.add(self.category3)
        self.film.directors.add(self.director3)

        self.film = Film(title='Різдво',
                         title_en='',
                         release_year=2022,
                         image='/Users/olegbondar/Python/project_django/Beetroot_django/media/images/155435585.jpg',
                         views='переглядів 367',
                         rating=8,
                         description="Описання фільму",
                         movie_link='https://www.youtube.com/watch?v=5PSNL1qE6VY',
                         trailer_link='https://www.youtube.com/watch?v=5PSNL1qE6VY',
                         slug='christmas-slug'
                         )
        self.film.save()
        self.film.categories.add(self.category1, self.category2, self.category3)
        self.film.directors.add(self.director4, self.director1)


    def test_translate_film(self):
        movies = Film.objects.all()
        translate_film(None, None, movies)
        movies = Film.objects.all()
        self.assertEqual(movies[0].title_en, 'Avatar')
