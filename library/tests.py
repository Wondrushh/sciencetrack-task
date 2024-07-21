import io

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from rest_framework.validators import ValidationError
from rest_framework.parsers import JSONParser
from rest_framework import status

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

    def test_get_one_author(self):
        """Test fetching books and comparing it with the DB data."""
        url = reverse("author-detail", args=[1])
        request = self.factory.get(url)
        request.user = self.user

        response = self.client.get(url)
        authors = Author.objects.get(pk=1)
        serializer = AuthorSerializer(authors, context={"request": request})

        self.assertEqual(response.data, serializer.data)

    def test_delete_author(self):
        """Test deleting an author."""
        url = reverse("author-detail", args=[1])
        request = self.factory.get(url)
        request.user = self.user

        # Delete the book and check if it was deleted
        response = self.client.delete(url)
        author_count = Author.objects.count()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(author_count, 0)

    def test_create_author(self):
        """Test creating a new author."""
        new_author = {
            "first_name": "Karel",
            "last_name": "Čapek",
            "birth_date": "1890-01-09",
        }
        url = reverse("author-list")
        response = self.client.post(url, new_author)
        self.assertEqual(response.status_code, 201)

        new_author_id = response.data["id"]
        response = self.client.get(reverse("author-detail", args=[new_author_id]))
        self.assertEqual(response.data["first_name"], new_author["first_name"])

    def test_partial_update_author(self):
        """Test modifying an author."""
        url = reverse("author-detail", args=[1])
        new_author_first_name = "Karel"

        response = self.client.patch(url, {"first_name": new_author_first_name})
        the_author = Author.objects.get(pk=1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(the_author.first_name, new_author_first_name)

    def test_full_update_author(self):
        """Test modifying an author using PUT method"""
        url = reverse("author-detail", args=[1])
        new_author = {
            "first_name": "Karel",
            "last_name": "Čapek",
            "birth_date": "1890-01-09",
        }

        response = self.client.put(url, new_author)
        the_author = Author.objects.get(pk=1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(the_author.first_name, new_author["first_name"])

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

    def test_get_one_book(self):
        """Test fetching a book and compare it with the DB data."""
        url = reverse("book-detail", args=[1])
        request = self.factory.get(url)
        request.user = self.user

        response = self.client.get(url)
        books = Book.objects.get(pk=1)
        serializer = BookSerializer(books, context={"request": request})

        self.assertEqual(response.data, serializer.data)

    def test_delete_book(self):
        """Test fetching books and compare it with the DB data."""
        url = reverse("book-detail", args=[1])
        request = self.factory.get(url)
        request.user = self.user

        # Delete the book and check if it was deleted
        response = self.client.delete(url)
        books_count = Book.objects.count()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(books_count, 0)

    def test_create_book(self):
        """Test creating a new book."""
        new_book = {
            "title": "Somebook",
            "isbn": "9788073901295",
            "pub_date": "2014-07-07",
            "authors": ["/api/authors/1/"],
        }
        url = reverse("book-list")
        response = self.client.post(url, new_book)
        self.assertEqual(response.status_code, 201)

        new_book_id = response.data["id"]
        response = self.client.get(reverse("book-detail", args=[new_book_id]))
        self.assertEqual(response.data["title"], new_book["title"])

    def test_partial_update_book(self):
        """Test modifying a book."""
        url = reverse("book-detail", args=[1])
        new_book_title = "Proti všem"

        response = self.client.patch(url, {"title": new_book_title})
        the_book = Book.objects.get(pk=1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(the_book.title, new_book_title)

    def test_full_update_book(self):
        """Test modifying a book using PUT method"""
        url = reverse("book-detail", args=[1])
        new_book = {
            "title": "Proti všem",
            "isbn": "978-80-907799-0-7",
            "pub_date": "2020-01-01",
            "authors": ["/api/authors/1/"],
        }

        response = self.client.put(url, new_book)
        the_book = Book.objects.get(pk=1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(the_book.title, new_book["title"])

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
