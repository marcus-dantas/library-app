import logging
import requests
from django.conf import settings
from typing import List, Dict, Optional
from books.models import Book

class GoogleBooksService:
    """
    Service class for interacting with Google Books API
    Handles searching, fetching, and converting Google Books data
    """
    
    BASE_URL = 'https://www.googleapis.com/books/v1/volumes'
    
    @classmethod
    def search_books(cls, query: str, max_results: int = 10) -> List[Dict]:
        """
        Search for books via Google Books API
        
        Args:
            query (str): Search term for books
            max_results (int): Maximum number of results to return
        
        Returns:
            List of book dictionaries from Google Books API
        """
        try:
            params = {
                'q': query,
                'maxResults': max_results,
                'key': settings.GOOGLE_BOOKS_API_KEY
            }
            response = requests.get(cls.BASE_URL, params=params)
            response.raise_for_status()
            
            return response.json().get('items', [])
        
        except requests.RequestException as e:
            logging.error(f"Google Books API error: {e}")
            return []
    
    @classmethod
    def convert_to_book_model(cls, google_book: Dict) -> Optional[Book]:
        """
        Convert Google Books API volume to Book model instance
        
        Args:
            google_book (Dict): Book data from Google Books API
        
        Returns:
            Book model instance or None if conversion fails
        """
        try:
            volume_info = google_book.get('volumeInfo', {})
            
            book_data = {
                'title': volume_info.get('title', 'Unknown Title'),
                'author': ', '.join(volume_info.get('authors', ['Unknown Author'])),
                'isbn': cls._extract_isbn(volume_info),
                'description': volume_info.get('description', ''),
                'google_book_id': google_book.get('id', ''),
            }
            
            book, created = Book.objects.get_or_create(
                isbn=book_data['isbn'],
                defaults=book_data
            )
            
            return book
        
        except Exception as e:
            logging.error(f"Book conversion error: {e}")
            return None
    
    @classmethod
    def _extract_isbn(cls, volume_info: Dict) -> str:
        """
        Extract ISBN from Google Books volume info
        
        Prioritizes ISBN_13, falls back to ISBN_10
        
        Args:
            volume_info (Dict): Volume information from Google Books
        
        Returns:
            ISBN as string, or empty string
        """
        identifiers = volume_info.get('industryIdentifiers', [])
        
        for identifier in identifiers:
            if identifier['type'] == 'ISBN_13':
                return identifier['identifier']
        
        for identifier in identifiers:
            if identifier['type'] == 'ISBN_10':
                return identifier['identifier']
        
        return ''

    @classmethod
    def import_books_from_search(cls, query: str, max_results: int = 10) -> List[Book]:
        """
        Search Google Books and import results to local database
        
        Args:
            query (str): Search term
            max_results (int): Maximum books to import
        
        Returns:
            List of imported Book instances
        """
        google_books = cls.search_books(query, max_results)
        imported_books = []
        
        for book_data in google_books:
            book = cls.convert_to_book_model(book_data)
            if book:
                imported_books.append(book)
        
        return imported_books
