from django.http import HttpResponse, HttpResponseBadRequest
from django.core import exceptions
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from .filters import SimpleGenericFilter


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all().order_by("-add_date")
    serializer_class = AuthorSerializer
    filter_backends = [SimpleGenericFilter]

    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all().order_by("-add_date")
    serializer_class = BookSerializer
    filter_backends = [SimpleGenericFilter]

    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]
