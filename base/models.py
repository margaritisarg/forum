from tkinter import CASCADE
from django.conf import settings
from django.db import models

class Post(models.Model):
    header = models.CharField(max_length=100)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)    
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.header