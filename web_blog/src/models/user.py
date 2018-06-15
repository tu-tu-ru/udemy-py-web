import datetime
import uuid

from flask import session

from src.common.database import Database
from src.models.blog import Blog


class User:
    # register
    # log in
    # create an account
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_from_mongo_by_email(cls, email):
        data = Database.find_one(collection='users', query={'email': email})
        # 上边这一行的末尾，用 email 的值，而不是用 self.email
        # 是因为这个时候只是找到了一个对应的 user，并没有生成一个 User class 的 object
        # 所以要用一个 class method
        if data is not None:
            return cls(**data)

    @classmethod
    def get_from_mongo_by_id(cls, _id):
        data = Database.find_one(collection='users', query={'_id': _id})
        if data is not None:
            return cls(**data)

    # 下边这个函数并没有用到 self，所以把它变成一个 staticmethod
    # Why?
    # 跟类有关系，但是又不会改变类和实例状态的方法，这种方法是静态方法，就使用 staticmethod 来装饰
    @staticmethod
    def login_valid(email, password):
        # To check whether the email and password match
        user = User.get_from_mongo_by_email(email)
        if user is not None:
            # Check whether the user_id and password match
            return user.password == password
            # password above is from the database
        else:
            return False

    @classmethod
    def register(cls, email, password):
        # if the user exists, the register will fail;
        user = cls.get_from_mongo_by_email(email)
        if user is None:
            # Then create a user --> Create a new instance of User class
            new_user = cls(email, password)
            new_user.save_to_mongo()
            session['email'] = email  # 注册完了之后自动登陆
            return True
        else:
            return False

    @staticmethod
    def login(user_email):
        # 在这里，用户名和密码都被确定是对的了
        # To actually login
        # Using `session` from Flask
        session['email'] = user_email

    @staticmethod
    def logout():
        session['email'] = None

    # 从数据库查找blog的时候如果用 author 查找，可能有重名的现象
    # solution：为每个 author 创建一个独一无二的 id （在 blog module 里）
    def get_blogs(self):
        return Blog.find_by_author_id(self._id)
        # FIXME
        # 为什么返回 Blog.find_by_author_id(self.author_id) 不行，参数得用 self._id ？

    def json(self):
        return {
            'email': self.email,
            '_id': self._id,
            'password': self.password
        }
        # BUT it's unsafe to send a password over network

    def save_to_mongo(self):
        Database.insert(collection='users', data=self.json())

    def new_blog(self, description, title):
        # 写新 blog 发生在 login 之后，所以我们就已经有了用户的各种信息
        # What do Blog class have:
        #   author, title, description, author_id
        blog = Blog(author=self.email,
                    author_id=self._id,
                    description=description,
                    title=title
                    )
        # author 和 author_id 都是从 User 对象里来的，所以直接用 self 就可以
        # title 和 description 是要用户后来添加的
        blog.save_to_mongo()

    # This method can be static
    def new_post(self, blog_id, title, content, date = datetime.datetime.now()):
        # Post 是发在 blog 里的，所以就先调用一个 blog 的对象
        blog = Blog.from_mongo(blog_id)
        blog.new_post(title=title,
                      content=content,
                      date=date)
        # new_post() method include a `save to mongodb method`
