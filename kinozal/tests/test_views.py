from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from kinozal.models import Category, Film
from kinozal.views import IndexViews
from kinozal.selectors import random_films_selector, max_rating_selector


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create(username='some_user')
        self.category1 = Category(name='comedy', slug='comedy-slug')
        self.category1.save()
        self.category2 = Category(name='action', slug='action-slug')
        self.category2.save()
        self.category3 = Category(name='melodrama', slug='melodrama-slug')
        self.category3.save()

        self.film = Film(title='Titan',
                         release_year=2002,
                         image='/Users/olegbondar/Python/project_django/'
                               'Beetroot_django/media/images/1538491614-1.jpg.jpg',
                         description="posting",
                         slug='django',
                         background='Users/olegbondar/Python/project_django/'
                               'Beetroot_django/media/images/1538491614-1.jpg.jpg'
                         )
        self.film.save()
        self.film.categories.add(self.category1)

    def test_IndexViews(self):

        response = self.client.get('/')
        view = IndexViews()
        view.setup(response)

        context = view.get_context_data()

        self.assertEqual(response.status_code, 200)
        self.assertIn('today_recomendation', context)
        self.assertEqual(response.context['today_recomendation'][0], random_films_selector()[0])
        self.assertEqual(response.context['max_rating'][0], max_rating_selector()[0])

    def test_SingleMoviesViews(self):

        response = self.client.get(reverse('single', args=(self.film.slug,)))
        self.assertEqual(response.status_code, 200)
        self.assertIn('related_films', response.context)


    def test_MoviesCategoryViews(self):

        response = self.client.get(reverse('category', args=(self.film.slug,)))
        self.assertEqual(response.status_code, 200)
        self.assertIn('years', response.context)

    def test_MoviesOlView(self):

        response = self.client.get(reverse('movies'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('top_film', response.context)

    def test_SearchView(self):

        response = self.client.get(reverse('search'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('top_film', response.context)
        self.assertIn('years', response.context)
