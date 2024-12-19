# test_backend.py
import os
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_project.settings')
django.setup()

from django.contrib.auth.models import User
from books.services.google_books import GoogleBooksService
from django.conf import settings

def test_google_books_api():
    """
    Test Google Books API integration
    """
    print("Testing Google Books API Integration:")
    try:
        books = GoogleBooksService.search_books("Python Programming")
        
        if not books:
            print("❌ No books found. Check API key and internet connection.")
            return False
        
        first_book = books[0]
        converted_book = GoogleBooksService.convert_to_book_model(first_book)
        
        if converted_book:
            print(f"✅ Successfully imported book: {converted_book.title}")
            return True
        else:
            print("❌ Failed to convert book")
            return False
    
    except Exception as e:
        print(f"❌ Google Books API Test Failed: {e}")
        return False

def test_user_authentication():
    """
    Test user authentication
    """
    print("\nTesting User Authentication:")
    try:
        username = 'testuser'
        password = 'testpassword123'
        
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(username=username, password=password)
            print("✅ Test user created")
        
        from django.contrib.auth import authenticate
        user = authenticate(username=username, password=password)
        
        if user:
            print("✅ Authentication successful")
            return True
        else:
            print("❌ Authentication failed")
            return False
    
    except Exception as e:
        print(f"❌ Authentication Test Failed: {e}")
        return False

def main():
    print("Starting Backend Testing...")
    
    google_books_test = test_google_books_api()
    
    auth_test = test_user_authentication()
    
    if google_books_test and auth_test:
        print("\n🎉 All Backend Tests Passed Successfully!")
    else:
        print("\n❌ Some Backend Tests Failed. Check configurations.")

if __name__ == '__main__':
    main()
