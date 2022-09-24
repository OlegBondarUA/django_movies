from django.shortcuts import render


def index(request):
    context = {}
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
