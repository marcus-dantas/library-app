from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from books.models import Book
from django.core.exceptions import ValidationError
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    full_name = models.CharField(max_length=255, blank=True)
    books_on_loan = models.ManyToManyField(
        Book,
        through='BookLoan',
        related_name='borrowers'
    )

    @property
    def is_admin(self):
        return self.user.is_staff
    
    @property
    def active_loans_count(self):
        return self.loans.filter(return_date__isnull=True).count()
    
    @property
    def has_overdue_books(self):
        return self.loans.filter(
            return_date__isnull=True,
            due_date__lt=timezone.now()
        ).exists()

    def __str__(self):
        return f"{self.user.username}'s profile"
    
    def get_active_loans(self):
        return self.loans.filter(return_date__isnull=True)
    
    def can_borrow_books(self):
        max_allowed_loans = 5
        return self.active_loans_count < max_allowed_loans

class BookLoan(models.Model):
    LOAN_STATUS = [
        ('ACTIVE', 'Active'),
        ('RETURNED', 'Returned'),
        ('OVERDUE', 'Overdue')
    ]

    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='loans'
    )
    book = models.ForeignKey(
        'books.Book',
        on_delete=models.CASCADE,
        related_name='loans'
    )
    loan_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=LOAN_STATUS, default='ACTIVE')

    class Meta:
        ordering = ['-loan_date']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'book'],
                condition=models.Q(return_date__isnull=True),
                name='unique_active_loan'
            )
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_return_date = self.return_date if self.pk else None

    def __str__(self):
        return f"{self.book.title} loaned to {self.user.user.username}"
    
    def clean(self):
        if not self.id:
            if self.book.available_copies < 1:
                raise ValidationError('This book is not available for loan.')
            if not self.user.can_borrow_books():
                raise ValidationError('User has reached maximum allowed loans.')
            if self.book.loans.filter(
                user=self.user,
                return_date__isnull=True
            ).exists():
                raise ValidationError('User already has this book on loan.')

    def save(self, *args, **kwargs):
        if not self.id:
            self.book.available_copies -= 1
            self.book.save()
        
        if not self.return_date:
            if self.due_date < timezone.now():
                self.status = 'OVERDUE'
            else:
                self.status = 'ACTIVE'
        else:
            self.status = 'RETURNED'
        
        super().save(*args, **kwargs)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(pre_save, sender=BookLoan)
def handle_returned_book(sender, instance, **kwargs):
    try:
        old_instance = BookLoan.objects.get(pk=instance.pk)
        if instance.return_date and not old_instance.return_date:
            instance.book.available_copies += 1
            instance.book.save()
    except BookLoan.DoesNotExist:
        pass

@receiver(post_save, sender=BookLoan)
def update_book_availability(sender, instance, created, **kwargs):
    if created:
        book = instance.book
        book.available_copies = max(0, book.available_copies - 1)
        book.save()
    elif instance.return_date and not instance._original_return_date:
        book = instance.book
        book.available_copies += 1
        book.save()
