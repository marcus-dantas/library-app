from django.core.management.base import BaseCommand
from books.services.google_books import GoogleBooksService

class Command(BaseCommand):
    help = 'Populate database with books from Google Books API'

    def add_arguments(self, parser):
        parser.add_argument('--topics', nargs='+', type=str,
                          default=['programming', 'fantasy', 'science fiction'],
                          help='List of topics to search for books')
        parser.add_argument('--books-per-topic', type=int, default=5,
                          help='Number of books to import per topic')

    def handle(self, *args, **options):
        topics = options['topics']
        books_per_topic = options['books_per_topic']
        
        total_imported = 0
        
        for topic in topics:
            self.stdout.write(f"Searching for '{topic}' books...")
            imported_books = GoogleBooksService.import_books_from_search(
                query=topic,
                max_results=books_per_topic
            )
            
            total_imported += len(imported_books)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully imported {len(imported_books)} books for topic '{topic}'"
                )
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                f"\nTotal books imported: {total_imported}"
            )
        )
