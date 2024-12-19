from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Book, BookRequest
from users.models import BookLoan
from .serializers import BookSerializer, BookDetailSerializer, BookCreateSerializer, BookRequestSerializer
from django.utils import timezone

BOOK_NOT_FOUND_ERROR = 'Book not found'

class BookListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_staff:
            return Response(
                {'error': 'Only admin users can create books'},
                status=status.HTTP_403_FORBIDDEN
            )
            
        serializer = BookCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
            serializer = BookDetailSerializer(book)
            return Response(serializer.data)
        except Book.DoesNotExist:
            return Response(
                {'error': BOOK_NOT_FOUND_ERROR},
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, pk):
        if not request.user.is_staff:
            return Response(
                {'error': 'Only admin users can update books'},
                status=status.HTTP_403_FORBIDDEN
            )
            
        try:
            book = Book.objects.get(pk=pk)
            serializer = BookCreateSerializer(book, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Book.DoesNotExist:
            return Response(
                {'error': BOOK_NOT_FOUND_ERROR},
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, pk):
        if not request.user.is_staff:
            return Response(
                {'error': 'Only admin users can delete books'},
                status=status.HTTP_403_FORBIDDEN
            )
            
        try:
            book = Book.objects.get(pk=pk)
            book.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Book.DoesNotExist:
            return Response(
                {'error': BOOK_NOT_FOUND_ERROR},
                status=status.HTTP_404_NOT_FOUND
            )
        
class BookRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Create a new book request"""
        book_id = request.data.get('book_id')
        notes = request.data.get('notes', '')

        try:
            book = Book.objects.get(id=book_id)
            
            existing_request = BookRequest.objects.filter(
                user=request.user.profile,
                book=book,
                status='PENDING'
            ).exists()

            if existing_request:
                return Response(
                    {'error': 'You already have a pending request for this book'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            book_request = BookRequest.objects.create(
                user=request.user.profile,
                book=book,
                notes=notes
            )

            serializer = BookRequestSerializer(book_request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Book.DoesNotExist:
            return Response(
                {'error': 'Book not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    def get(self, request):
        """Get user's book requests"""
        requests = BookRequest.objects.filter(user=request.user.profile)
        serializer = BookRequestSerializer(requests, many=True)
        return Response(serializer.data)

class AdminBookRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_staff:
            return Response(
                {'error': 'Admin access required'},
                status=status.HTTP_403_FORBIDDEN
            )

        requests = BookRequest.objects.all()
        serializer = BookRequestSerializer(requests, many=True)
        return Response(serializer.data)

    def put(self, request, request_id):
        if not request.user.is_staff:
            return Response(
                {'error': 'Admin access required'},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            book_request = BookRequest.objects.get(id=request_id)
            new_status = request.data.get('status')
            
            if new_status not in ['APPROVED', 'REJECTED']:
                return Response(
                    {'error': 'Invalid status'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            book_request.status = new_status
            book_request.response_date = timezone.now()
            book_request.save()

            if new_status == 'APPROVED' and book_request.book.available_copies > 0:
                due_date = timezone.now() + timezone.timedelta(days=14)
                BookLoan.objects.create(
                    user=book_request.user,
                    book=book_request.book,
                    due_date=due_date
                )

            serializer = BookRequestSerializer(book_request)
            return Response(serializer.data)

        except BookRequest.DoesNotExist:
            return Response(
                {'error': 'Request not found'},
                status=status.HTTP_404_NOT_FOUND
            )
