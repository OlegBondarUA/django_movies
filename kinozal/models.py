from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=35, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Director(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=250, unique=True)

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
    duration = models.CharField(max_length=50, null=True)
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

    def __str__(self):
        return self.title


class Comment(models.Model):
    films = models.ForeignKey(Film, null=True, on_delete=models.CASCADE,
                              related_name='comments')
    comment = models.TextField(default='')

    def __str__(self):
        return self.comment
