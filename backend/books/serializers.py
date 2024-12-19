from rest_framework import serializers
from .models import Book, BookRequest

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'author',
            'isbn',
            'description',
            'google_book_id',
            'total_copies',
            'available_copies'
        ]

class BookDetailSerializer(serializers.ModelSerializer):
    is_available = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'author',
            'isbn',
            'description',
            'google_book_id',
            'total_copies',
            'available_copies',
            'is_available'
        ]
    
    def get_is_available(self, obj):
        return obj.available_copies > 0

class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'title',
            'author',
            'isbn',
            'description',
            'total_copies'
        ]
        
    def create(self, validated_data):
        validated_data['available_copies'] = validated_data['total_copies']
        return super().create(validated_data)

class BookRequestSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.user.username', read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)
    
    class Meta:
        model = BookRequest
        fields = [
            'id',
            'username',
            'book_title',
            'request_date',
            'status',
            'notes',
            'response_date'
        ]
        read_only_fields = ['request_date', 'response_date', 'status']
