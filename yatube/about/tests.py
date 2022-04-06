from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class StaticURLTests(TestCase):
    def test_about_urls(self):
        """Проверка доступности адресов /author/, /tech/."""
        urls = [
            reverse('about:author'),
            reverse('about:tech'),
        ]
        for address in urls:
            with self.subTest(address=address):
                response = self.client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_about_url_uses_correct_template(self):
        """Проверка шаблонов для адресов  /author/, /tech/."""
        templates_url_names = {
            reverse('about:author'): 'about/author.html',
            reverse('about:tech'): 'about/tech.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(template=template):
                response = self.client.get(address)
                self.assertTemplateUsed(response, template)
