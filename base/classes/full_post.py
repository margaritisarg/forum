from django.db import models

class Full_post_comment(models.Model):
    comment_id = models.IntegerField()
    comment_body = models.TextField()
    comment_post_id = models.TextField()
    comment_user_id = models.TextField()
    user_username = models.TextField()

    def __str__(self):
        return self.comment_body

    def __eq__(self, other):
        return self.comment_id == other.comment_id

    def __hash__(self):
        return hash((self.comment_body))