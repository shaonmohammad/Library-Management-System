# Generated by Django 5.1.4 on 2024-12-20 08:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('author', models.CharField(max_length=255)),
                ('publication_date', models.DateField(blank=True, null=True)),
                ('isbn', models.CharField(max_length=13, unique=True)),
                ('copies_available', models.PositiveIntegerField(default=1)),
                ('total_copies', models.PositiveIntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='BorrowRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrow_date', models.DateField(auto_now_add=True)),
                ('return_deadline', models.DateField()),
                ('returned_date', models.DateField(blank=True, null=True)),
                ('overdue_fine', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='borrow_records', to='api.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='borrowed_books', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
