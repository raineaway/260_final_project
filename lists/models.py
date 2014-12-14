from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Item(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    )
    user = models.ForeignKey(User)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default='pending')
    due_date = models.DateTimeField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

