from django.contrib import admin
from .models import Book,BorrowRecord
# Register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title','author','publication_date','total_copies','is_available')

@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ('user','book','borrow_date','return_deadline','returned_date','overdue_fine')