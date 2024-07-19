import io

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from rest_framework.validators import ValidationError
from rest_framework.parsers import JSONParser

from .views import AuthorViewSet
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


class AuthorEndpointTests(APITestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.user = User.objects.create_superuser(username="admin", password="admin")
        self.client.login(username="admin", password="admin")

        # Create some objects to play with
        self.author = Author.objects.create(
            first_name="Alois", last_name="Jirásek", birth_date="1886-01-01"
        )
        return super().setUp()

    def test_get_authors(self):
        url = reverse("author-list")
        request = self.factory.get(url)
        request.user = self.user

        response = self.client.get(url)
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True, context={"request": request})
        # print(serializer.data)
        # print(response.data["results"])

        self.assertEqual(response.data["results"], serializer.data)

    def test_is_birth_date_in_the_past(self):
        """The birth date of the author should be in the past."""
        new_author = {
            "first_name": "Future",
            "last_name": "Human",
            "birth_date": "2200-01-01",
        }
        url = reverse("author-list")

        self.assertEqual(
            self.client.post(url, new_author, format="json").status_code, 400
        )


class BookEndpointTests(APITestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.user = User.objects.create_superuser(username="admin", password="admin")
        self.client.login(username="admin", password="admin")

        # Create some testing db objects
        self.author = Author.objects.create(
            first_name="Alois", last_name="Jirásek", birth_date="1886-01-01"
        )
        self.book = Book.objects.create(
            title="Psohlavci", isbn="9788073901295", pub_date="2014-07-07"
        )

        # Assign the author to the book
        self.book.authors.set([self.author])
        return super().setUp()

    def test_get_books(self):
        """Test fetching books and comparing it with the DB data."""
        url = reverse("book-list")
        request = self.factory.get(url)
        request.user = self.user

        response = self.client.get(url)
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True, context={"request": request})

        self.assertEqual(response.data["results"], serializer.data)

    def test_is_pub_date_in_the_past(self):
        """The birth date of the author should be in the past."""
        new_book = {
            "title": "Somebook",
            "isbn": "9788073901295",
            "pub_date": "2222-01-01",
            "authors": ["/api/authors/1/"],
        }
        url = reverse("book-list")

        self.assertEqual(
            self.client.post(url, new_book, format="json").status_code, 400
        )

    def test_isbn_validation(self):
        """The ISBN should be valid."""
        new_book = {
            "title": "Somebook",
            "isbn": "9788073901295",
            "pub_date": "2014-07-07",
            "authors": ["/api/authors/1/"],
        }
        url = reverse("book-list")
        response = self.client.post(url, new_book)

        self.assertEqual(response.status_code, 201)

    def test_isbn_validation_invalid(self):
        """The ISBN should be invalid"""
        new_book = {
            "title": "Somebook",
            "isbn": "9788073901296",
            "pub_date": "2014-07-07",
            "authors": ["/api/authors/1/"],
        }
        url = reverse("book-list")
        response = self.client.post(url, new_book)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["isbn"][0], "Invalid ISBN.")

    def test_remove_hyphens_from_isbn(self):
        """The BookSerializer should remove the hyphens from the ISBN before saving it."""
        new_book = {
            "title": "Somebook",
            "isbn": "978-8073901295",
            "pub_date": "2014-07-07",
            "authors": ["/api/authors/1/"],
        }
        url = reverse("book-list")
        response = self.client.post(url, new_book)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["isbn"], "9788073901295")
