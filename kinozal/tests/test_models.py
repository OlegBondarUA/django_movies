from django.test import TestCase
from kinozal.models import (
    Film,
    Category,
    Country,
    Comment,
    Actor,
    Director
)


class FirstTestCase(TestCase):

    def setUp(self):
        self.categories = ['action', 'comedy', 'drama']
        for category in self.categories:
            self.obj = Category.objects.create(
                name=category,
                slug=category + '-slug'
            )

    def test_add_categories_and_get_objects(self):

        objs = Category.objects.all()
        slugs = Category.objects.values_list('slug', flat=True).get(pk=1)

        self.assertEqual(objs.count(), 3)
        self.assertEqual(slugs, 'action-slug')

    def test_string_representation(self):

        category = Category(name='My category name')
        self.assertEqual(str(category), category.name)

    def test_verbose_name_plural(self):
        self.assertEqual(str(Category._meta.verbose_name_plural), "Categories")
