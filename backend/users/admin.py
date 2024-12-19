from django.contrib import admin
from .models import UserProfile, BookLoan

class BookLoanInline(admin.TabularInline):
    model = BookLoan
    extra = 0
    readonly_fields = ('loan_date',)
    fields = ('book', 'loan_date', 'due_date', 'return_date')
    can_delete = True


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_admin', 'active_loans_count']
    search_fields = ['user__username', 'user__email']
    inlines = [BookLoanInline]

    def username(self, obj):
        return obj.user.username

    def email(self, obj):
        return obj.user.email

    def active_loans_count(self, obj):
        return obj.loans.filter(return_date__isnull=True).count()
    active_loans_count.short_description = 'Active Loans'
    
@admin.register(BookLoan)
class BookLoanAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'loan_date', 'due_date', 'return_date']
    list_filter = ['return_date', 'due_date']
    search_fields = ['user__user__username', 'book__title']
    raw_id_fields = ['user', 'book']
