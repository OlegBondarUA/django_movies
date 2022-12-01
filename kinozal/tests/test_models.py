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

    def test_add_categories_and_get_all_objects(self):

        categories = ['action', 'comedy', 'drama']
        for category in categories:
            obj = Category.objects.create(
                name=category,
                slug=category+'slug'

            )
            self.assertEqual(category, obj.name)

        objs = Category.objects.all()
        slugs = Category.objects.get(slug='actionslug')
        print('slug: ', slugs)

        self.assertEqual(objs.count(), 3)
        self.assertEqual(slugs, 'action')
