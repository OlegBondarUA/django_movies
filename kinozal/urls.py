"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views
urlpatterns = [
    path('', views.IndexViews.as_view(), name='index'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('movies/', views.MoviesOlView.as_view(), name='movies'),
    path('movies/<slug:slug>/', views.MoviesCategoryViews.as_view(), name='category'),
    path('single-movies/<slug:slug>/', views.SingleMoviesViews.as_view(), name='single'),
    path("review/<int:pk>/", views.AddReview.as_view(), name="add_review"),
]
