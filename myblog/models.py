from django.db import models
from tinymce.models import HTMLField
import os

# Create your models here.

class User(models.Model):

    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=50, unique=True,verbose_name='邮箱')
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to=os.path.join('myblog','image'), null=True,default='myblog/image/1.png' )

    def __str__(self):
        return self.username


class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150)
    content = HTMLField()
    pub_date = models.DateTimeField()
    mod_date = models.DateTimeField(null=True)
    is_delete = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
