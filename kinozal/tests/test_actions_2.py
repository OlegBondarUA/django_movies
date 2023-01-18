from django.test import TestCase
from unittest.mock import patch

from kinozal.models import Film
from kinozal.actions import translate_film


class TranslateFilmTest(TestCase):
    def setUp(self):
        # Create a test model object
        self.obj = Film.objects.create(
            title='Test title',
            description='Test description',
            views='Test views',
            slug='test-title',
        )

    @patch('deep_translator.GoogleTranslator.translate_batch')
    def test_translate_film(self, translate_batch_mock):
        # Set up mock return value for translate_batch function
        translate_batch_mock.return_value = (
        'Translated Title', 'Translated Description', 'Translated Views')

        # Call the translate_film function with the test object
        translate_film(None, None, [self.obj])

        # Assert that the object's fields have been correctly updated
        self.assertEqual(self.obj.title_en, 'Translated Title')
        self.assertEqual(self.obj.description_en, 'Translated Description')
        self.assertEqual(self.obj.views_en, 'Translated Views')


    @patch('deep_translator.GoogleTranslator.translate_batch',
           side_effect=Exception('Test exception'))
    def test_translate_film_error(self, translate_batch_mock):
        # Call the translate_film function with the test object
        translate_film(None, None, [self.obj])

        # Assert that the object's fields have not been updated
        self.assertEqual(self.obj.title_en, '')
        self.assertEqual(self.obj.description_en, '')
        self.assertEqual(self.obj.views_en, '')