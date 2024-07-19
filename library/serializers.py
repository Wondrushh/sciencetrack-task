from rest_framework import serializers
from .models import Author, Book
from .validators import PastDateTimeValidator, ISBNValidator


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    birth_date = serializers.DateField(validators=[PastDateTimeValidator()])
    class Meta:
        model = Author
        fields = ["id", "url", "first_name", "last_name", "birth_date"]


class BookSerializer(serializers.HyperlinkedModelSerializer):
    isbn = serializers.CharField(validators=[ISBNValidator()])
    pub_date = serializers.DateField(validators=[PastDateTimeValidator()])
    
    def create(self, validated_data):
        # Remove hyphens from the ISBN
        validated_data["isbn"] = validated_data["isbn"].replace("-", "")

        return super().create(validated_data)

    class Meta:
        model = Book
        fields = ["id", "url", "title", "isbn", "pub_date", "authors"]
