from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Genre(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField()
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='books')
    borrowed = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Borrow(models.Model):
    date_borrowed = models.DateTimeField(auto_now=True)
    borrower = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    returned = models.BooleanField(default=False)
