from django.db import models

class Author(models.Model):
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    birth_date = models.DateField()

class Book(models.Model):
    title = models.CharField(max_length=120)
    isbn = models.CharField(max_length=17) # 17 chars = ISBN13 with hyphens
    pub_date = models.DateField("date published")    
    authors = models.ManyToManyField(Author)

