

def sql_post_join(user_id):
    post_join = f" SELECT a.[username], b.[header], b.[body] FROM ( SELECT [header], [body], [user_id] FROM base_post WHERE user_id = {user_id} ) b INNER JOIN auth_user a ON b.user_id = a.id "
    return post_join

