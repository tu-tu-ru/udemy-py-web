import datetime
import uuid

from database import Database
from models.post import Post


class Blog:
    def __init__(self, author, title, description, id=None):
        self.author = author
        self.title = title
        self.description = description
        self.id = uuid.uuid4().hex if id is None else id

    def new_post(self):
        title = input("Input the title: ")
        content = input("Type your content: ")
        date = input("Date of the post (DDMMYYYY): ")
        if date == "":
            date = str(datetime.datetime.now())[8:10] + str(datetime.datetime.now())[5:7] + str(datetime.datetime.now())[0:4]
        post = Post(blog_id=self.id,
                    title=title,
                    content=content,
                    date=datetime.datetime.strptime(date, "%d%m%Y"),
                    author=self.author)
        # 注意上边的 self 是 Blog 的，因为现在还在 Blog class 里

        post.save_to_mongo()

    # This function is like the from_blog function
    def get_posts(self):
        return Post.from_blog(self.id)

    def save_to_mongo(self):
        Database.insert(collection='blogs', data=self.json())

    def json(self):
        return {
            'author': self.author,
            'title': self.title,
            'description': self.description,
            'id': self.id
        }

    # 可以把这个 function 设置成 classmethod
    # 如果以后对 return 的这个 obj 有什么改动，就不必要手动改 class name 了
    # 函数内部没有 self

    @classmethod
    def from_mongo(cls, id):
        blog_data = Database.find_one(collection='blogs',
                                      query={'id': id})
        # Then return an instance of Blog, using the properties of blog_data (get from database)
        # We do not return raw data, but an object
        return cls(author=blog_data['author'],
                   title=blog_data['title'],
                   description=blog_data['description'],
                   id=blog_data['id'])