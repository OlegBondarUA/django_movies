from django.contrib import admin

from . models import Category, Director, Actor, Film, Comment


class FilmAdmin(admin.ModelAdmin):
    list_display = 'title'
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category)
admin.site.register(Director)
admin.site.register(Actor)
admin.site.register(Film)
admin.site.register(Comment)
