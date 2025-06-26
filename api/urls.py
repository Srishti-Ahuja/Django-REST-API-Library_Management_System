from django.contrib import admin
from django.urls import path, include
from .views import BookList, BookDetail, GenreList, GenreDetail, BookByGenre, BookBorrow, BookReturn, BorrowList

urlpatterns = [
    path('books/', BookList.as_view()),
    path('books/<int:pk>/', BookDetail.as_view()),
    path('borrowlist/', BorrowList.as_view()),
    path('genre/', GenreList.as_view()),
    path('<str:title>/', GenreDetail.as_view()),
    path('<str:title>/books/', BookByGenre.as_view()),
    path('books/<int:pk>/borrow/', BookBorrow.as_view()),
    path('books/<int:pk>/return/', BookReturn.as_view())
]
