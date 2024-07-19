from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all().order_by("-add_date")
    serializer_class = AuthorSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all().order_by("-add_date")
    serializer_class = BookSerializer
