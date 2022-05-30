

def sql_post_join(user_id):
    post_join = f" SELECT a.[username], b.[header], b.[body], b.[id] FROM ( SELECT [header], [body], [created], [id], [user_id] FROM base_post WHERE user_id = {user_id} ) b INNER JOIN auth_user a ON b.user_id = a.id ORDER BY b.[created] DESC"
    return post_join

