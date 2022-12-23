from random import sample

from django.db.models import QuerySet

from .models import Film, Category


def random_films_selector(films_number: int = 8) -> QuerySet[Film]:
    film_ids = Film.objects.values_list('pk', flat=True)
    random_ids = sample(list(film_ids), min(films_number, len(film_ids)))
    return Film.objects.prefetch_related(
        'categories').filter(pk__in=random_ids)


def max_rating_selector(from_film: int = 0, to_film: int = 5) -> QuerySet[Film]:
    return Film.objects.order_by('-rating')[from_film:to_film]


def categories_selector() -> QuerySet[Category]:
    films = Film.objects.all()
    return Category.objects.filter(
        films__in=films).distinct().order_by('name')


def years_selector() -> QuerySet[Film]:
    return Film.objects.values_list(
        'release_year', flat=True).distinct().order_by('-release_year')


def related_film_selector(film: Film) -> QuerySet[Film]:
    related_films = Film.objects.filter(
        categories__id__in=film.categories.all()
    ).values_list('id', flat=True)
    random_ids = sample(list(related_films), min(6, len(related_films)))
    return Film.objects.prefetch_related(
        'categories').filter(pk__in=random_ids)


def related_director_selector(film: Film) -> QuerySet[Film]:
    related_director = Film.objects.filter(
        directors__id__in=film.directors.all()
    ).values_list('id', flat=True)
    return Film.objects.prefetch_related(
        'directors').filter(pk__in=list(related_director))
