from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView,
        UpdateAPIView, ListAPIView)
from .models import Book, Genre, Borrow
from .serializer import (BookSerializer, BookByGenreSerializer, GenreSerializer,
        UserSerializer, BookBorrowSerializer, BookReturnSerializer, BorrowSerializer)
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from .throttling import BookThrottle, BorrowThrottle

# Create your views here.
class BookList(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    throttle_classes = (BookThrottle,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class BookDetail(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsOwnerOrReadOnly, )
    throttle_classes = (BookThrottle,)

class BookByGenre(ListCreateAPIView):
    serializer_class = BookByGenreSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        genre = self.kwargs['title']
        return Book.objects.filter(genre__title=genre)

    def perform_create(self, serializer):
        genre = get_object_or_404(Genre, title = self.kwargs['title'])
        serializer.save(author=self.request.user, genre=genre)

class GenreList(ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class GenreDetail(RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'title__iexact'
    lookup_url_kwarg = 'title'

class BookBorrow(CreateAPIView):
    queryset = Borrow.objects.all()
    serializer_class = BookBorrowSerializer
    permission_classes = (IsAuthenticated,)
    throttle_classes = (BorrowThrottle, )

    def perform_create(self, serializer):
        book = get_object_or_404(Book, pk=self.kwargs['pk'])
        serializer.save(book = book, borrower = self.request.user)

class BookReturn(UpdateAPIView):
    queryset = Borrow.objects.all()
    serializer_class = BookReturnSerializer
    permission_classes = (IsAuthenticated,)
    throttle_classes = (BorrowThrottle, )

    def perform_update(self, serializer):
        serializer.save(returned=True)

class BorrowList(ListAPIView):
    queryset = Borrow.objects.all()
    serializer_class = BorrowSerializer

@api_view(['POST'])
def RegistrationView(request):
    if request.method=='POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()

            token = RefreshToken.for_user(account)

            data = {
                'account' : account,
                'token' : {
                    'refresh' : str(token),
                    'access' : str(token.access_token)
                }
            }

            return Response(data, status=201)
        return Response(serializer.errors)
