import unittest
from unittest import mock

from kinozal.actions import translate_film


class TranslateFilmTest(unittest.TestCase):
    @mock.patch('deep_translator.GoogleTranslator.translate_batch')
    def test_translate_film(self, mock_translate_batch):
        # set up test data
        mock_translate_batch.return_value = ['Title (en)', 'Description (en)', 'Views (en)']
        obj = mock.Mock()
        obj.title = 'Title (uk)'
        obj.description = 'Description (uk)'
        obj.views = 'Views (uk)'
        obj.title_en = ''
        obj.description_en = ''
        obj.views_en = ''

        # call the function
        translate_film(None, None, [obj])

        # assert the results
        self.assertEqual(obj.title_en, 'Title (en)')
        self.assertEqual(obj.description_en, 'Description (en)')
        self.assertEqual(obj.views_en, 'Views (en)')
