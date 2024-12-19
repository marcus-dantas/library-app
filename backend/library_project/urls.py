from django.contrib import admin
from django.urls import path, include
from users.views import LoginView, LogoutView, RegisterView, UserViewSet, LoanViewSet, CurrentUserView, UserListView
from books.views import BookListView, BookDetailView, BookRequestView, AdminBookRequestView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'loans', LoanViewSet, basename='loan')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/auth/logout/', LogoutView.as_view(), name='logout'),
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/users/me/', CurrentUserView.as_view(), name='current-user'),
    path('api/users/', UserListView.as_view(), name='user-list'),
    path('api/books/', BookListView.as_view(), name='book-list'),
    path('api/books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('api/book-requests/', BookRequestView.as_view(), name='book-requests'),
    path('api/admin/book-requests/', AdminBookRequestView.as_view(), name='admin-book-requests'),
    path('api/admin/book-requests/<int:request_id>/', AdminBookRequestView.as_view(), name='admin-book-request-detail'),
    path('', include(router.urls)),
]
