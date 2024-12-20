from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import (
    BookListAPIView,
    BookCreateAPIView,
    BookUpdateAPIView,
    BookDeleteAPIView,
    BorrowBookAPIView,
    ReturnBookAPIView,
    UserBorrowRecordsAPIView
)
urlpatterns = [

    # JWT Authentication Endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Book Management Endpoints
    path('books/', BookListAPIView.as_view(), name='books-list'),
    path('books/create/', BookCreateAPIView.as_view(), name='books-create'),
    path('books/<int:pk>/update/', BookUpdateAPIView.as_view(), name='books-update'),
    path('books/<int:pk>/delete/', BookDeleteAPIView.as_view(), name='books-delete'),
    path('books/<int:book_id>/borrow/', BorrowBookAPIView.as_view(), name='books-borrow'),
    path('books/<int:book_id>/return/',ReturnBookAPIView.as_view(), name='books-return'),
    path('books/borrow-records/', UserBorrowRecordsAPIView.as_view(), name='user-borrow-records'),

]