from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.views.generic import TemplateView, ListView, DetailView

from . models import Film
from . import selectors


class IndexViews(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {
            'today_recomendation': selectors.random_films_selector(),
            'max_rating': selectors.max_rating_selector(),
            'max_rating2': selectors.max_rating_selector(6, 12),
        }
        return context


class SingleMoviesViews(DetailView):
    template_name = 'single-movies.html'
    model = Film
    context_object_name = 'film'
    slug_url_kwarg = 'slug'
    queryset = Film.objects.prefetch_related('categories')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {
            'related_films': selectors.related_film_selector(self.object),
            'related_director': selectors.related_director_selector(self.object),
        }
        return context


class MoviesCategoryViews(ListView):
    template_name = 'movies.html'
    model = Film
    context_object_name = 'films'
    slug_url_kwarg = 'slug'
    paginate_by = 30

    def get(self, request, *args, **kwargs):
        self.year = int(self.request.GET['release_year'])\
            if self.request.GET.get('release_year') else None
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        _filter = {
            'categories__slug': self.kwargs.get('slug')
        }

        if self.year:
            _filter['release_year'] = self.year

        return Film.objects.prefetch_related('categories').filter(**_filter)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context |= {
            'years': selectors.years_selector(),
            'top_film': selectors.max_rating_selector(10, 15),
        }
        return context


class MoviesOlView(ListView):
    template_name = 'movies.html'
    model = Film
    paginate_by = 30
    context_object_name = 'films'

    def get(self, request, *args, **kwargs):
        self.year = int(self.request.GET['release_year'])\
            if self.request.GET.get('release_year') else None
        return super().get(request, *args, **kwargs)

    def get_queryset(self):

        if self.year:
            _filter = {
                'release_year': self.year
            }
            return Film.objects.prefetch_related('categories').filter(**_filter)
        else:
            return Film.objects.prefetch_related('categories')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {
            'years': selectors.years_selector(),
            'top_film': selectors.max_rating_selector(10, 15),
        }
        return context


class SearchView(ListView):
    template_name = 'movies.html'
    model = Film
    context_object_name = 'films'
    paginate_by = 30
    search_query = None

    def get(self, request, *args, **kwargs):
        self.search_query = self.request.GET.get('q')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):

        return Film.objects.prefetch_related(
            'categories').annotate(rank=self._create_search_rank()).filter(
            rank__gte=0.3).distinct().order_by('-rank')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context |= {
            'years': selectors.years_selector(),
            'top_film': selectors.max_rating_selector(10, 15),
        }
        return context

    def _create_search_rank(self) -> SearchRank:
        if self.request.LANGUAGE_CODE == 'en-us':
            vector = SearchVector('title_en', weight='A') \
                     + SearchVector('release_year', weight='A') \
                     + SearchVector('directors__name_en', weight='A') \
                     + SearchVector('actors__name_en', weight='A') \
                     + SearchVector('categories__name_en', weight='A')

            query = SearchQuery(self.search_query)
            rank = SearchRank(
                vector,
                query,
            )
        else:
            vector = SearchVector('title', weight='A') \
                     + SearchVector('release_year', weight='A') \
                     + SearchVector('directors__name', weight='A') \
                     + SearchVector('actors__name', weight='A') \
                     + SearchVector('categories__name', weight='A') \

            query = SearchQuery(self.search_query)
            rank = SearchRank(
                vector,
                query,
             )
        return rank
