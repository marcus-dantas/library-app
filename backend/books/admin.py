from django.contrib import admin
from .models import Book, BookRequest
from django.utils import timezone

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'available_copies')
    search_fields = ('title', 'author', 'isbn')
    list_filter = ('available_copies',)

@admin.register(BookRequest)
class BookRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'request_date', 'status', 'response_date']
    list_filter = ['status', 'request_date', 'response_date']
    search_fields = ['user__user__username', 'book__title']
    readonly_fields = ['request_date']
    actions = ['approve_requests', 'reject_requests']

    def approve_requests(self, request, queryset):
        queryset.update(
            status='APPROVED',
            response_date=timezone.now()
        )
    approve_requests.short_description = "Approve selected requests"

    def reject_requests(self, request, queryset):
        queryset.update(
            status='REJECTED',
            response_date=timezone.now()
        )
    reject_requests.short_description = "Reject selected requests"
