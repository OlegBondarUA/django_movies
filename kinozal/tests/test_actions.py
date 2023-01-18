from django.test import TestCase
from unittest import mock
from unittest.mock import patch
import time

from kinozal.models import Film
from kinozal.actions import translate_film


class TranslateFilmTestLogic(TestCase):
    def setUp(self):
        self.test_obj1 = Film.objects.create(
            title='Test title 1',
            description='Test description 1',
            views='Test views 1',
            slug='test-title-1',
        )
        self.test_obj2 = Film.objects.create(
            title='Test title 2',
            description='Test description 2',
            views='Test views 2',
            slug='test-title-2',
        )
        self.test_queryset = Film.objects.filter(id__in=[self.test_obj1.id, self.test_obj2.id])

    def test_translate_film_calls_translate_object(self):
        with mock.patch('kinozal.actions.translate_object') as mock_translate_object:
            translate_film(None, None, self.test_queryset)
            mock_translate_object.assert_has_calls([mock.call(self.test_obj1),
                                                    mock.call(self.test_obj2)], any_order=True)
            self.assertEqual(mock_translate_object.call_count, 2)

    def test_error_handling(self):
        with mock.patch('deep_translator.GoogleTranslator.translate_batch',
                        side_effect=Exception(
                                'Test exception')), self.assertLogs('logit',
                                                                    level='ERROR') as log:
            translate_film(None, None, self.test_queryset)
            # Check that the exception message was logged
            self.assertIn('ERROR:logit:translate - Test title 1 -> Test exception',
                          log.output[0])
            self.assertIn('ERROR:logit:translate - Test title 1 -> Test exception',
                          log.output[0])
