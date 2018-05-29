from database import Database
from models.blog import Blog
from models.post import Post

Database.initialize()

my_blog = Blog(author="Big bear", title="Bear article", description="This some description")

my_blog.new_post()

my_blog.save_to_mongo()

data_from_db = my_blog.from_mongo(id=my_blog.id)  # 这里需要的 id 是 my_posy 的 id 属性对应的数值

print(my_blog.get_posts())

# 用这个输入的内容可以在 mongodb 里用 `db.posts.find({})` 查看