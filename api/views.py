from datetime import date
from django.db import transaction, IntegrityError
from django.shortcuts import render,get_list_or_404
from .models import Book,BorrowRecord
from .custom_permission import IsAdminUser,IsMemberUser

from .serializer import BookSerializer,BorrowRecordSerializer

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# List API View
class BookListAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# Create API View
class BookCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# Update API View
class BookUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'pk' 

# Delete API View
class BookDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'pk' 


class BorrowBookAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request,book_id, *args, **kwargs):
        
        try:
            # Validate book ID and fetch the book
            book = Book.objects.select_for_update().get(id=book_id)
        except Book.DoesNotExist:
            return Response({"detail": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Wrap in a transaction for concurrency safety
            with transaction.atomic():
                
                # Check availability again under the transaction
                if not BorrowRecord.is_book_available(book):
                    return Response({"detail": "No copies available for this book."}, status=status.HTTP_400_BAD_REQUEST)

                # Check if the user can borrow more books
                if not BorrowRecord.can_borrow(request.user):
                    return Response({"detail": "Borrow limit reached. Return a book to borrow another."}, status=status.HTTP_400_BAD_REQUEST)

                if not book.is_available:
                     return Response({"details":"The book has been borrowed from the library"},status=status.HTTP_400_BAD_REQUEST)
                
                # Create the borrow record
                BorrowRecord.objects.create(user=request.user, book=book)

                # Update the book's available copies
                book.total_copies -= 1
                book.is_available = False
                book.save()

        except IntegrityError:
            # Handle database integrity errors
            return Response({"detail": "An error occurred while borrowing the book. Please try again."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"detail": f"You have successfully borrowed '{book.title}'."}, status=status.HTTP_201_CREATED)

class ReturnBookAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request,book_id,*args, **kwargs):
        try:
            # Get the book
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"detail": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

        
        try:
            borrow_record = BorrowRecord.objects.filter(book_id=book_id, user=request.user).last()
            if borrow_record.returned_date:
                return Response({"details":"The book already returned"},status=status.HTTP_400_BAD_REQUEST)
            borrow_record.returned_date =  date.today()
            borrow_record.save()

        except BorrowRecord.DoesNotExist:
            return Response({"detail":"Not found borrow record for this book."}, status=status.HTTP_404_NOT_FOUND)
        
        # Updates the availability status
        book.is_available = True
        book.save()
 
        return Response({"detail": f"You have successfully return book name: '{book.title}'."}, status=status.HTTP_201_CREATED)


class UserBorrowRecordsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Fetch borrow records for the authenticated user
        borrow_records = BorrowRecord.objects.filter(user=request.user)

        if not borrow_records.exists():
            return Response({"detail": "No borrow records found."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the borrow records
        serializer = BorrowRecordSerializer(borrow_records, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)