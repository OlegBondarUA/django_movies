from django.test import SimpleTestCase
from django.urls import reverse, resolve
from kinozal.views import (
    IndexViews,
    SingleMoviesViews,
    MoviesCategoryViews,
    MoviesOlView,
    SearchView
)


class TestUrls(SimpleTestCase):

    def test_index_url_is_resolved(self):
        url = reverse('index')
        self.assertEqual(resolve(url).func.view_class, IndexViews)

    def test_search_url_is_resolved(self):
        url = reverse('search')
        self.assertEqual(resolve(url).func.view_class, SearchView)

    def test_movies_url_is_resolved(self):
        url = reverse('movies')
        self.assertEqual(resolve(url).func.view_class, MoviesOlView)

    def test_category_url_is_resolved(self):
        url = reverse('category', args=['some-slug'])
        self.assertEqual(resolve(url).func.view_class, MoviesCategoryViews)

    def test_single_url_is_resolved(self):
        url = reverse('single', args=['some-slug'])
        self.assertEqual(resolve(url).func.view_class, SingleMoviesViews)
