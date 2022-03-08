from django.db import models
from django.conf import settings 
from django.contrib.auth.models import User

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     username = models.TextField(max_length=10)

class AnonyPost(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, null=True, default='', on_delete=models.CASCADE)
    anony = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class AnonyComment(models.Model):
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(AnonyPost, null=True, blank=True, on_delete=models.CASCADE)
    author =  models.ForeignKey(User, null=True, blank=True,on_delete=models.CASCADE) 

    class Meta:
      ordering = ['-date'] #댓글 최신순

    def __str__(self):
        return self.comment

class FreePost(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author =  models.ForeignKey(User, on_delete=models.CASCADE) 
    anony = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class FreeComment(models.Model):
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author =  models.ForeignKey(User, null=True, blank=True,on_delete=models.CASCADE, related_name='freecomment_author') #익명이 아니므로 저자 있어야함
    post = models.ForeignKey(FreePost, null=True, blank=True, on_delete=models.CASCADE, related_name='freecomment_post')

    def __str__(self):
        return self.comment