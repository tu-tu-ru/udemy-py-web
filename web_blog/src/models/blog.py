import datetime
import uuid

from src.common.database import Database
from src.models.post import Post


class Blog:
    def __init__(self, author, title, description, author_id, _id=None):
        self.author = author
        self.title = title
        self.description = description
        self._id = uuid.uuid4().hex if _id is None else _id
        # 对于这个 self.id，mongodb会给每一个记录一个 "_id"，他的类型是一个 objectId
        # 我们可以把 id 这个变量的名字改成 _id，以便覆盖掉 mongodb 生成的那个ObjId
        self.author_id = author_id

    def new_post(self, title, content, date=datetime.datetime.now()):
        post = Post(blog_id=self._id,
                    title=title,
                    content=content,
                    created_date=datetime.datetime.strptime(date, "%d%m%Y"),
                    author=self.author)
        # 注意上边的 self 是 Blog 的，因为现在还在 Blog class 里

        post.save_to_mongo()

    # This function is like the from_blog function
    def get_posts(self):
        return Post.from_blog(self._id)

    def save_to_mongo(self):
        Database.insert(collection='blogs', data=self.json())

    def json(self):
        return {
            'author': self.author,
            'title': self.title,
            'description': self.description,
            '_id': self._id,
            'author_id': self.author_id
        }

    # 可以把这个 function 设置成 classmethod
    # 如果以后对 return 的这个 obj 有什么改动，就不必要手动改 class name 了
    # 函数内部没有 self

    @classmethod
    def from_mongo(cls, id):
        blog_data = Database.find_one(collection='blogs',
                                      query={'_id': id})
        # Then return an instance of Blog, using the properties of blog_data (get from database)
        # We do not return raw data, but an object
        return cls(**blog_data)
        #return type(blog_data)
        # 这一串儿返回值等价于 return cls(**blog_data)

    @classmethod
    def find_by_author_id(cls, author_id):
        blogs_found = Database.find(collection='blogs', query={'author_id': author_id})
        # 上边这行是返回 a list of blogs
        #return [blog for blog in blogs_found]
        #  这样是返回了一个大的列表，里边包括的是每个 blog 的小列表
        # 但是想要的是以对象为形式的每个 blog
        return [cls(**blog) for blog in blogs_found]
