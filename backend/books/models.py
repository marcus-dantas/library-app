from django.db import models
from django.core.exceptions import ValidationError

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    description = models.TextField(blank=True)
    google_book_id = models.CharField(max_length=100, blank=True)
    total_copies = models.IntegerField(default=1)
    available_copies = models.IntegerField(default=1)

    def __str__(self):
        return self.title

    def clean(self):
        if self.available_copies > self.total_copies:
            raise ValidationError('Available copies cannot exceed total copies')
        if self.available_copies < 0:
            raise ValidationError('Available copies cannot be negative')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class BookRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('CANCELLED', 'Cancelled')
    ]

    user = models.ForeignKey(
        'users.UserProfile',
        on_delete=models.CASCADE,
        related_name='book_requests'
    )
    book = models.ForeignKey(
        'Book',
        on_delete=models.CASCADE,
        related_name='requests'
    )
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    notes = models.TextField(blank=True)
    response_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-request_date']

    def __str__(self):
        return f"Request for {self.book.title} by {self.user.user.username}"
