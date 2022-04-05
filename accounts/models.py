from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class extendedUser(models.Model):
    profile_pic = models.FileField(default='default.jpg', upload_to='profilepics')
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
