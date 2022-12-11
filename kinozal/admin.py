from django.contrib import admin
from django.utils.html import format_html, mark_safe
from django_summernote.admin import SummernoteModelAdmin

from .actions import translate_film, translate_name
from . models import Category, Director, Actor, Film, Comment, Country


class FilmAdmin(SummernoteModelAdmin):
    actions = (translate_film,)
    summernote_fields = ('description', 'description_en')
    list_display = ('title', 'translated', 'picture')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'release_year')
    list_filter = ('country', 'rating', 'release_year')

    fieldsets = (
        (None, {
            'fields': (
                'base_url', 'slug',
                ('title', 'title_en'),
                ('image',),
                ('background',),
                ('description',),
                ('description_en',),
                ('views', 'views_en'),
                ('rating', 'release_year'),
                ('movie_link',),
                ('trailer_link',),
            )
        }),
    )

    @staticmethod
    def picture(obj):
        return format_html(
            '<img src="{}" style="max-width: 50px">', obj.image.url
        )

    @staticmethod
    def translated(obj):
        if obj.title_en and obj.description_en and obj.duration_en:
            return mark_safe(
                '<img src="/static/admin/img/icon-yes.svg" alt=True>')
        return mark_safe(
            '<img src="/static/admin/img/icon-no.svg" alt="False">')


class CategoryAdmin(admin.ModelAdmin):
    actions = (translate_name,)
    list_display = ('name', 'name_en', 'slug', 'total_films')
    search_fields = ('name',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('films')

    @staticmethod
    def total_films(obj):
        count = obj.films.count()
        link = f'/admin/kinozal/film/?categories__id__exact={obj.id}'
        return format_html(f'<a href="{link}">{count} films</a>')


class CountryAdmin(admin.ModelAdmin):
    list_display = ('country', 'total_films')
    search_fields = ('country',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('films')

    @staticmethod
    def total_films(obj):
        count = obj.films.count()
        link = f'/admin/kinozal/film/?country__id__exact={obj.id}'
        return format_html(f'<a href="{link}">{count} films</a>')


class DirectorAdmin(admin.ModelAdmin):
    actions = (translate_name,)
    list_display = ('name', 'name_en', 'total_films')
    search_fields = ('name',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('films')

    @staticmethod
    def total_films(obj):
        count = obj.films.count()
        link = f'/admin/kinozal/film/?director__id__exact={obj.id}'
        return format_html(f'<a href="{link}">{count} films</a>')


class ActorAdmin(admin.ModelAdmin):
    actions = (translate_name,)
    list_display = ('name', 'name_en', 'total_films')
    search_fields = ('name',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('films')

    @staticmethod
    def total_films(obj):
        count = obj.films.count()
        link = f'/admin/kinozal/film/?actor__id__exact={obj.id}'
        return format_html(f'<a href="{link}">{count} films</a>')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Director, DirectorAdmin)
admin.site.register(Actor, ActorAdmin)
admin.site.register(Film, FilmAdmin)
admin.site.register(Comment)
admin.site.register(Country, CountryAdmin)
