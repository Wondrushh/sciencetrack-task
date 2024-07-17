from rest_framework import serializers
from .models import Author, Book


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "url", "first_name", "last_name", "birth_date"]


class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "url", "title", "isbn", "pub_date", "authors"]
