from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.decorators import action
from .serializers import UserSerializer, BookLoanSerializer
from .models import BookLoan, UserProfile
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import authenticate, login, logout
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from books.models import Book
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        
        if user:
            login(request, user)
            return Response({
                'user_id': user.id,
                'username': user.username,
                'is_admin': user.is_staff,
                'profile': UserSerializer(user.profile).data
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'message': 'Successfully logged out'})

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        errors = {}

        if not username:
            errors['username'] = 'Username is required'
        elif User.objects.filter(username=username).exists():
            errors['username'] = 'Username already exists'
        elif len(username) < 3:
            errors['username'] = 'Username must be at least 3 characters long'

        if not email:
            errors['email'] = 'Email is required'
        else:
            try:
                validate_email(email)
                if User.objects.filter(email=email).exists():
                    errors['email'] = 'Email already in use'
            except ValidationError:
                errors['email'] = 'Invalid email format'

        if not password:
            errors['password'] = 'Password is required'
        elif len(password) < 8:
            errors['password'] = 'Password must be at least 8 characters long'
        elif password != confirm_password:
            errors['confirm_password'] = 'Passwords do not match'

        if errors:
            return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(
                username=username, 
                email=email, 
                password=password
            )

            user.is_active = True
            user.save()

            authenticated_user = authenticate(
                username=username, 
                password=password
            )
            
            if authenticated_user:
                login(request, authenticated_user)

            return Response({
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'is_admin': user.is_staff
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'error': 'An error occurred during registration',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UserViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=user.id)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return super().get_permissions()

    @action(detail=True, methods=['get'])
    def loans(self, request, pk=None):
        try:
            user = self.get_object()
            loans = BookLoan.objects.filter(user=user.profile)
            serializer = BookLoanSerializer(loans, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['get'])
    def active_loans(self, request, pk=None):
        try:
            user = self.get_object()
            active_loans = BookLoan.objects.filter(
                user=user.profile,
                return_date__isnull=True
            )
            serializer = BookLoanSerializer(active_loans, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class LoanViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BookLoanSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return BookLoan.objects.all()
        return BookLoan.objects.filter(user=user.profile)

    def create(self, request):
        book_id = request.data.get('book_id')
        user_id = request.data.get('user_id')

        try:
            book = Book.objects.get(id=book_id)
            
            if request.user.is_staff and user_id:
                user_profile = UserProfile.objects.get(id=user_id)
            else:
                user_profile = request.user.profile

            if not user_profile.can_borrow_books():
                return Response(
                    {'error': 'User has reached maximum allowed loans'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if book.available_copies < 1:
                return Response(
                    {'error': 'Book not available'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            due_date = timezone.now() + timedelta(days=14)
            loan = BookLoan.objects.create(
                user=user_profile,
                book=book,
                due_date=due_date
            )

            return Response(
                BookLoanSerializer(loan).data,
                status=status.HTTP_201_CREATED
            )

        except (Book.DoesNotExist, UserProfile.DoesNotExist):
            return Response(
                {'error': 'Invalid book or user ID'},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        try:
            loan = self.get_object()
            if loan.return_date:
                return Response(
                    {'error': 'Book already returned'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            loan.return_date = timezone.now()
            loan.save()

            return Response(BookLoanSerializer(loan).data)
        except BookLoan.DoesNotExist:
            return Response(
                {'error': 'Loan not found'},
                status=status.HTTP_404_NOT_FOUND
            )

class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user:
            return User.objects.all()
        return User.objects.filter(id=user.id)
