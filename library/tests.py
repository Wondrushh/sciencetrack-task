from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from rest_framework.validators import ValidationError

from .views import AuthorViewSet
from .models import Author, Book


class AuthorEndpointTests(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_superuser(username="admin", password="admin")
        self.client.login(username="admin", password="admin")

        # Create some objects to play with
        self.author = Author.objects.create(first_name="Alois", last_name="Jirásek", birth_date="1886-01-01")
        return super().setUp()

    def test_get_authors(self):
        url = reverse("author-list")

        response = self.client.get(url)
        print(response.content)

    def test_is_birth_date_in_the_past(self):
        """The birth date of the author should be in the past."""
        new_author = {
            "first_name": "Future",
            "last_name": "Human",
            "birth_date": "2200-01-01",
        }
        url = reverse("author-list")

        self.assertEqual(self.client.post(url, new_author, format="json").status_code, 400) 

class BookEndpointTests(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_superuser(username="admin", password="admin")
        self.client.login(username="admin", password="admin")
        return super().setUp()

    def test_is_pub_date_in_the_past(self):
        """The birth date of the author should be in the past."""
        new_book = {
            "title": "Somebook",
            "isbn": "1234",
            "pub_date": "2222-01-01",
        }
        url = reverse("book-list")

        self.assertEqual(self.client.post(url, new_book, format="json").status_code, 400) 
