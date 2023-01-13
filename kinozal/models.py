from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=35, unique=True)
    name_en = models.CharField(max_length=50, default='')
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Director(models.Model):
    name = models.CharField(max_length=50, unique=True)
    name_en = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=250, unique=True)
    name_en = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.name


class Country(models.Model):
    country = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.country


class Film(models.Model):
    base_url = models.URLField(max_length=512, null=True, blank=True)
    title = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255, default='')
    slug = models.SlugField(max_length=255, unique=True)
    release_year = models.PositiveSmallIntegerField(null=True)
    views = models.CharField(max_length=50, null=True)
    views_en = models.CharField(max_length=50, default='')
    rating = models.FloatField(max_length=5, null=True)
    description = models.TextField(default='')
    description_en = models.TextField(default='')
    image = models.ImageField(upload_to='images', null=True, blank=True)
    movie_link = models.URLField(max_length=255, null=True, blank=True)
    trailer_link = models.URLField(max_length=255, null=True, blank=True)
    data_created = models.DateTimeField(auto_now_add=True)
    background = models.ImageField(upload_to='background', null=True, blank=True)

    country = models.ManyToManyField(Country, related_name='films')
    categories = models.ManyToManyField(Category, related_name='films')
    directors = models.ManyToManyField(Director, related_name='films')
    actors = models.ManyToManyField(Actor, related_name='films')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("single", kwargs={"slug": self.slug})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

class Reviews(models.Model):
    """Comments"""
    email = models.EmailField()
    name = models.CharField("name", max_length=100)
    text = models.TextField("message", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="parent", on_delete=models.SET_NULL, blank=True, null=True
    )
    film = models.ForeignKey(Film, verbose_name="film", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.film}"

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"