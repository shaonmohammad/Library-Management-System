from rest_framework import serializers, generics
from .models import Book,BorrowRecord


# Serializers
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class BorrowRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRecord
        fields = ['id', 'book', 'borrow_date', 'return_deadline',"returned_date","overdue_fine"]
        depth = 1  