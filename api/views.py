from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Book, Genre
from .serializer import BookSerializer, GenreSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
class BookList(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDetail(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class GenreList(ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class GenreDetail(RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'title__iexact'
    lookup_url_kwarg = 'title'

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
