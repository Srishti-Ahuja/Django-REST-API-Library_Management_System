from django.contrib import admin
from django.urls import path, include
from .views import BookList, BookDetail, GenreList, GenreDetail, BookByGenre

urlpatterns = [
    path('books/', BookList.as_view()),
    path('books/<int:pk>/', BookDetail.as_view()),
    path('genre/', GenreList.as_view()),
    path('<str:title>/', GenreDetail.as_view()),
    path('<str:title>/<int:pk>', BookByGenre.as_view())
]
