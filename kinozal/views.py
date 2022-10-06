from django.shortcuts import render

from . models import Film, Category


def index(request):
    category = Category.objects.all()
    films = Film.objects.all()
    today_recomendation = Film.objects.order_by('-release_year')[9:17]
    max_rating = Film.objects.order_by('-rating')[:5]
    max_rating2 = Film.objects.order_by('-rating')[6:13]
    context = {
        'today_recomendation': today_recomendation,
        'category': category,
        'max_rating': max_rating,
        'max_rating2': max_rating2,
        'films': films
    }

    return render(request, 'index.html', context)


def movies(request):
    context = {}
    return render(request, 'movies.html', context)


def single_movies(request):
    context = {}
    return render(request, 'single-movies-v7.html', context)


def error_404(request):
    context = {}
    return render(request, '404.html', context)
