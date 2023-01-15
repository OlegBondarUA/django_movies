from django.test import TestCase
from kinozal.forms import ReviewForm

class ReviewFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'text': 'This is a great film!'
        }
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_missing_name(self):
        form_data = {
            'email': 'johndoe@example.com',
            'text': 'This is a great film!'
        }
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['name'], ['This field is required.'])

    def test_missing_email(self):
        form_data = {
            'name': 'John Doe',
            'text': 'This is a great film!'
        }
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['This field is required.'])

    def test_missing_text(self):
        form_data = {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
        }
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], ['This field is required.'])

    def test_invalid_email(self):
        form_data = {
            'name': 'Test User',
            'email': 'invalid',
            'text': 'Review text'
        }
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['Enter a valid email address.'])
