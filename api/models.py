from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta,date

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.CharField(max_length=255)
    publication_date = models.DateField(null=True, blank=True)
    isbn = models.CharField(max_length=13, unique=True)
    is_available = models.BooleanField(default=True)
    total_copies = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.title} by {self.author}"

class BorrowRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="borrowed_books")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrow_records")
    borrow_date = models.DateField(auto_now_add=True)
    return_deadline = models.DateField()
    returned_date = models.DateField(null=True, blank=True)
    overdue_fine = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        if not self.return_deadline:
            # 14 days deadline
            self.return_deadline = date.today() + timedelta(days=14)  

        if self.returned_date and self.returned_date > self.return_deadline:
            overdue_days = (self.returned_date - self.return_deadline).days
            # 5 BDT per day fine
            self.overdue_fine = overdue_days * 5  
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"

    @staticmethod
    def can_borrow(user):
        return BorrowRecord.objects.filter(user=user, returned_date__isnull=True).count() < 5

    @staticmethod
    def is_book_available(book):
        return book.total_copies > 0
