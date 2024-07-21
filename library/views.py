from django.http import HttpResponse, HttpResponseBadRequest
from django.core import exceptions
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from .filters import SimpleGenericFilter


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all().order_by("-add_date")
    serializer_class = AuthorSerializer

    def get_queryset(self):
        queryset = super(AuthorViewSet, self).get_queryset()
        return self.apply_filters(queryset)


class BookViewSet(ModelViewSet, SimpleGenericFilter):
    queryset = Book.objects.all().order_by("-add_date")
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = super(BookViewSet, self).get_queryset()
        return self.apply_filters(queryset)
        