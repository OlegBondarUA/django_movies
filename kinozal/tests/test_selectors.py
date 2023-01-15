from django.contrib.auth import get_user_model
from django.test import TestCase

from kinozal.selectors import (
    random_films_selector,
    max_rating_selector,
    categories_selector,
    years_selector,
    related_film_selector,
    related_director_selector
)
from kinozal.models import Category, Film, Director


class TestSelectors(TestCase):
    # Preparation of textual data
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


        self.film = Film(title='avatar',
                         release_year=2002,
                         image='/Users/olegbondar/Python/project_django/Beetroot_django/media/images/255798820.jpg',
                         views=100,
                         rating=9,
                         description="posting",
                         movie_link='https://www.youtube.com/watch?v=5PSNL1qE6VY',
                         trailer_link='https://www.youtube.com/watch?v=5PSNL1qE6VY',
                         slug='avatar-slug'
                         )

        self.film.save()
        self.film.categories.add(self.category2)
        self.film.directors.add(self.director1)

        self.film = Film(title='alone at home',
                         release_year=1992,
                         image='/Users/olegbondar/Python/project_django/Beetroot_django/media/images/15249323.jpg',
                         views=756,
                         rating=7,
                         description="posting",
                         movie_link='https://www.youtube.com/watch?v=5PSNL1qE6VY',
                         trailer_link='https://www.youtube.com/watch?v=5PSNL1qE6VY',
                         slug='alone-at-home-slug'
                         )
        self.film.save()
        self.film.categories.add(self.category1)
        self.film.directors.add(self.director2)

        self.film = Film(title='titanic',
                         release_year=2000,
                         image='/Users/olegbondar/Python/project_django/Beetroot_django/media/images/49150562.jpg',
                         views=567,
                         rating=6,
                         description="posting",
                         movie_link='https://www.youtube.com/watch?v=5PSNL1qE6VY',
                         trailer_link='https://www.youtube.com/watch?v=5PSNL1qE6VY',
                         slug='titanic-slug'
                         )
        self.film.save()
        self.film.categories.add(self.category3)
        self.film.directors.add(self.director3)

        self.film = Film(title='christmas',
                         release_year=2022,
                         image='/Users/olegbondar/Python/project_django/Beetroot_django/media/images/155435585.jpg',
                         views=367,
                         rating=8,
                         description="posting",
                         movie_link='https://www.youtube.com/watch?v=5PSNL1qE6VY',
                         trailer_link='https://www.youtube.com/watch?v=5PSNL1qE6VY',
                         slug='christmas-slug'
                         )
        self.film.save()
        self.film.categories.add(self.category1, self.category2, self.category3)
        self.film.directors.add(self.director4, self.director1)

    def test_random_films_selector(self):
        # Test with default films_number (4)
        films = random_films_selector()
        self.assertEqual(films.count(), 4)
        self.assertEqual(len(films), len(set(films)))

        # Test with films_number=2
        films = random_films_selector(films_number=2)
        self.assertEqual(films.count(), 2)
        self.assertEqual(len(films), len(set(films)))

        # Test with films_number > number of films in db
        films = random_films_selector(films_number=10)
        self.assertEqual(films.count(), 4)  # four films in the setUp
        self.assertEqual(len(films), len(set(films)))

        # Test with empty db
        Film.objects.all().delete()
        films = random_films_selector()
        self.assertEqual(films.count(), 0)
        self.assertEqual(len(films), len(set(films)))

    def test_max_rating_selector(self):
        # Test with default films_number (4)
        films = max_rating_selector()
        self.assertEqual(films.count(), 4)
        for film in films:
            self.assertGreaterEqual(film.rating, films[3].rating)
        # Test with films_number=2
        films = max_rating_selector(1, 3)
        self.assertEqual(films.count(), 2)
        for film in films:
            self.assertGreaterEqual(film.rating, films[1].rating)
        # Test with films_number > number of films in db
        films = max_rating_selector(0, 10)
        self.assertEqual(films.count(), 4)  # four films in the setUp
        for film in films:
            self.assertGreaterEqual(film.rating, films[3].rating)
        # Test with empty db
        Film.objects.all().delete()
        films = max_rating_selector()
        self.assertEqual(films.count(), 0)

    def test_categories_selector(self):
        # Test with default films_number (3)
        films = categories_selector()
        self.assertEqual(films.count(), 3)
        self.assertEqual(films[0].slug, self.category2.slug)

        # Test with empty db
        Film.objects.all().delete()
        films = categories_selector()
        self.assertEqual(films.count(), 0)

    def test_years_selector(self):
        # Test with default films_number (4)
        films = years_selector()
        self.assertEqual(films.count(), 4)
        self.assertEqual(films[3], 1992)
        # Test with films_number=2
        films = years_selector()[0:2]
        self.assertEqual(films.count(), 2)
        self.assertEqual(films[1], 2002)
        # Test with films_number > number of films in db
        films = years_selector()[0:10]
        self.assertEqual(films.count(), 4)  # four films in the setUp
        self.assertEqual(films[0], 2022)
        # Test with empty db
        Film.objects.all().delete()
        films = years_selector()
        self.assertEqual(films.count(), 0)

    def test_related_film_selector(self):
        # Test with default films_number (4)
        films = related_film_selector(self.film)
        self.assertEqual(films.count(), 4)
        self.assertEqual(films[0].categories.first().name, 'action')
        self.assertEqual(films[1].categories.first().name, 'comedy')
        # Test with films_number=2
        films = related_film_selector(self.film)[1:3]
        self.assertEqual(films.count(), 2)
        self.assertEqual(films[0].categories.first().name, 'comedy')
        self.assertEqual(films[1].categories.first().name, 'melodrama')
        # Test with films_number > number of films in db
        films = related_film_selector(self.film)[0:10]  # four films in the setUp
        self.assertEqual(films.count(), 4)
        self.assertEqual(films[0].categories.first().name, 'action')
        self.assertEqual(films[1].categories.first().name, 'comedy')
        # Test with empty db
        Film.objects.all().delete()
        films = related_film_selector(self.film)
        self.assertEqual(films.count(), 0)

    def test_related_director_selector(self):
        # Test with default films_number (4)
        films = related_director_selector(self.film)
        self.assertEqual(films.count(), 2)
        self.assertEqual(films[0].title, 'avatar')
        self.assertEqual(films[1].title, 'christmas')
        # Test with films_number=1
        films = related_director_selector(self.film)[:1]
        self.assertEqual(films.count(), 1)
        self.assertEqual(films[0].title, 'avatar')
        # Test with films_number > number of films in db
        films = related_director_selector(self.film)[:10]  # two films in the setUp
        self.assertEqual(films.count(), 2)
        self.assertEqual(films[0].title, 'avatar')
        self.assertEqual(films[1].title, 'christmas')
        # Test with empty db
        Film.objects.all().delete()
        films = related_director_selector(self.film)
        self.assertEqual(films.count(), 0)
