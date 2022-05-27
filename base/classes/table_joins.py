from tkinter import CASCADE
from django.conf import settings
from django.db import models

class Post_joined_user(models.Model):
    header = models.TextField()
    body = models.TextField()
    user = models.TextField()

    def __str__(self):
        return self.header
