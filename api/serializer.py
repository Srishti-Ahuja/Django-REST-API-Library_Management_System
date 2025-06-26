from rest_framework import serializers
from .models import Book, Genre, Borrow
from django.contrib.auth.models import User

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = ('author',)

class BookByGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = ('author','genre',)

class GenreSerializer(serializers.ModelSerializer):
    books = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = Genre
        fields = '__all__'

class BorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrow
        fields = '__all__'

class BookBorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrow
        exclude = ('book', 'borrower',)

    def save(self, book, borrower):
        if Borrow.objects.filter(book = book, returned = False).exists():
            raise serializers.ValidationError('This book is already borrowed')
        if Borrow.objects.filter(borrower = borrower, returned = False).exists():
            raise serializers.ValidationError('This user already has 1 book borrowed')
            
        return super().save(book=book, borrower=borrower)

class BookReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrow
        exclude = ('book', 'borrower', 'returned',)

class UserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True, style={'input_type':'password'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm')
        extra_kwargs = {
            'password':{'write_only':True}
        }

        def save(self):
            username = self.validated_data['username']
            email = self.validated_data['email']
            password = self.validated_data['password']
            password_confirm = self.validated_data['password_confirm']

            if password!=password_confirm:
                raise serializers.ValidationError('Passwords are not matching')

            if User.objects.filter(username=username).exists():
                raise serializers.ValidationError('Use a unique username')

            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError('This email is already registered')

            account = User(email=email, username=username)
            account.set_password(password)
            account.save()

            return account
