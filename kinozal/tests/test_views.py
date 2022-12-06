# from django.test import TestCase, Client
# from django.urls import reverse
# from kinozal.models import (
#     Film,
#     Category,
#     Country,
#     Comment,
#     Actor,
#     Director
# )
# import json
#
#
# class TestViews(TestCase):
#
#     def setUp(self):
#         self.client = Client()
#         self.index_url = reverse(/single/, args=['uves-ce-dzaz'])
#
#     def test_IndexViews_GET(self):
#         response = self.client.get(self.index_url)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'kinozal/project-single.html')