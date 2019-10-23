from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100) # TODO: Implement choices set for category
    details = models.TextField()
    location = models.TextField()
    event_date = models.DateTimeField()

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
