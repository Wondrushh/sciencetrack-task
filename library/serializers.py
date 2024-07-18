from rest_framework import serializers
from .models import Author, Book
from .validators import PastDateTime


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    birth_date = serializers.DateField(validators=[PastDateTime()])
    class Meta:
        model = Author
        fields = ["id", "url", "first_name", "last_name", "birth_date"]


class BookSerializer(serializers.HyperlinkedModelSerializer):
    pub_date = serializers.DateField(validators=[PastDateTime()])
    class Meta:
        model = Book
        fields = ["id", "url", "title", "isbn", "pub_date", "authors"]
