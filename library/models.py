import datetime

from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    birth_date = models.DateField()
    add_date = models.DateTimeField("date added", auto_now_add=True)
    
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    title = models.CharField(max_length=120)
    isbn = models.CharField(max_length=17)  # 17 chars = ISBN13 with hyphens
    pub_date = models.DateField("date published")
    authors = models.ManyToManyField(Author)
    add_date = models.DateTimeField("date added", auto_now_add=True)
    
    def __str__(self) -> str:
        return self.title