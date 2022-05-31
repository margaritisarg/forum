from tkinter import CASCADE
from django.conf import settings
from django.db import models

class Post(models.Model):
    header = models.CharField(max_length=100)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)    
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.header

class Comment(models.Model):
    body = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)    
    created = models.DateTimeField(auto_now_add=True)    
    
    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.header

