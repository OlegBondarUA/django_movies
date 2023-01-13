from django.test import TestCase
from kinozal.models import Film, Category, Director, Actor, Country, Reviews

class FilmModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='action', slug='action')
        self.director = Director.objects.create(name='John Doe')
        self.actor = Actor.objects.create(name='Jane Doe')
        self.country = Country.objects.create(country='USA')

        self.film = Film.objects.create(
            title='Test Film',
            release_year=2020,
            views='1000',
            rating=8.5,
            description='Test description',
            image='test.jpg',
            movie_link='https://test.com',
            trailer_link='https://test.com/trailer',
            slug='test-film'
        )
        self.film.categories.add(self.category)
        self.film.directors.add(self.director)
        self.film.actors.add(self.actor)
        self.film.country.add(self.country)

    def test_film_model(self):
        self.assertEqual(self.film.title, 'Test Film')
        self.assertEqual(self.film.release_year, 2020)
        self.assertEqual(self.film.views, '1000')
        self.assertEqual(self.film.rating, 8.5)
        self.assertEqual(self.film.description, 'Test description')
        self.assertEqual(self.film.image.url, '/media/test.jpg')
        self.assertEqual(self.film.movie_link, 'https://test.com')
        self.assertEqual(self.film.trailer_link, 'https://test.com/trailer')
        self.assertEqual(self.film.categories.first(), self.category)
        self.assertEqual(self.film.directors.first(), self.director)
        self.assertEqual(self.film.actors.first(), self.actor)
        self.assertEqual(self.film.country.first(), self.country)
        self.assertEqual(self.film.get_absolute_url(), '/single-movies/test-film/')

class ReviewsModelTest(TestCase):
    def setUp(self):
        self.film = Film.objects.create(title='Test Film')
        self.review = Reviews.objects.create(
            email='test@example.com',
            name='Test User',
            text='Test review',
            film=self.film
        )

    def test_reviews_model(self):
        self.assertEqual(self.review.email, 'test@example.com')
        self.assertEqual(self.review.name, 'Test User')
        self.assertEqual(self.review.text, 'Test review')
        self.assertEqual(self.review.film, self.film)

