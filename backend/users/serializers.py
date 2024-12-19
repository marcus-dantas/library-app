from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils import timezone
from .models import UserProfile, BookLoan
from books.serializers import BookSerializer

class BookLoanSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    user_name = serializers.CharField(source='user.user.username', read_only=True)
    days_remaining = serializers.SerializerMethodField()
    
    class Meta:
        model = BookLoan
        fields = ['id', 'book', 'user_name', 'loan_date', 'return_date', 'due_date', 'status', 'days_remaining']
    
    def get_days_remaining(self, obj):
        if obj.return_date:
            return 0
        if obj.due_date:
            remaining = (obj.due_date - timezone.now()).days
            return max(0, remaining)
        return None

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    active_loans = BookLoanSerializer(
        source='loans',
        many=True,
        read_only=True
    )
    loans = serializers.SerializerMethodField()
    can_borrow = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'full_name', 'is_admin', 'active_loans', 'loans', 'can_borrow']
    
    def get_is_admin(self, obj):
        return obj.is_staff

    def get_active_loans(self, obj):
        active_loans = obj.loans.filter(return_date__isnull=True)
        return BookLoanSerializer(active_loans, many=True).data

    def get_loans(self, obj):
        completed_loans = obj.loans.filter(return_date__isnull=False)
        return BookLoanSerializer(completed_loans, many=True).data

    def get_can_borrow(self, obj):
        return obj.can_borrow_books()

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff','profile']
