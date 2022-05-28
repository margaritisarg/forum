from django.db import models
from django.db import connection
from ..sql.queries import sql_post_join

class Post_user(models.Model):
    header = models.TextField()
    body = models.TextField()
    user = models.TextField()

    def return_user_post_join(user_id):
        cursor = connection.cursor()
        cursor.execute(sql_post_join(user_id))
        results = cursor.fetchall()

        results_list = []
        for result in results:
            post_user = Post_user()
            post_user.user = result[0]
            post_user.header = result[1]
            post_user.body = result[2]
            results_list.append(post_user)
        return results_list

    def __str__(self):
        return self.header
