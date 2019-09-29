from django.db import models

# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100) # TODO: Implement choices set for category
    details = models.TextField()
    '''
    User
    Date
    Other fields to implement:
    Recurring days
    Club/ Group edit permissions
    Image
    '''
    def __str__(self):
        return self.name
