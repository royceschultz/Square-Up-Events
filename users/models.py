from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    # follows = models.ManyToManyField('self', related_name='follows', symmetrical=False)

    def __str__(self):
        return f'{self.user.username} Profile'

class Contact(models.Model):
    user_from = models.ForeignKey(User, related_name='rel_from_set') # The one that follows
    user_to = models.ForeignKey(User, related_name='rel_to_set') # The one that is followed
    created = models.DateTimeField( auto_now_add= True, db_index= True ) #stores time Db query  increased performance

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.user_from,self.user_to)

#Add following field to User dynamically by Monkeypatching
User.add_to_class('following', models.ManyToManyField('self',through =Contact, related_name = 'followers', symmetrical = False))
