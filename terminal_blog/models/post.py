import uuid

from database import Database

import datetime


class Post:
    def __init__(self, title, content, author, blog_id, date=datetime.datetime.now(), post_id=None):
        # Parameter with default value can only be put in the end
        self.title = title
        self.content = content
        self.author = author
        self.blog_id = blog_id
        self.post_id = uuid.uuid4().hex if post_id is None else post_id
        # The default value of post_id is None
        # 要 import uuid 先
        # uuid() is a method to generate a uuid which is unique
        # .hex gives a 32-bit string
        self.create_date = date

    def save_to_mongo(self):
        Database.insert(collection="posts",
                        data=self.json())
    # What is Database?
    #   Database is a class
    # How to use insert() method?

    def json(self):
        return {
            'post_id': self.post_id,
            'title': self.title,
            'content': self.content,
            'author': self.author,
            'blog_id': self.blog_id,
            'create_date': self.create_date
        }
        # 返回一个 json 文件

    # return the mongo ID from the mongo database
    @staticmethod
    def from_mongo(id):
        return Database.find_one(collection='posts', query={'post_id': id})  # query 的功能是找到一个 post 对应的 'id' 是参数里的这个 id

    #
    @staticmethod
    def from_blog(id):
        result = Database.find(collection='posts', query={'blog_id': id})  # result is a pymongo cursor
        return [i for i in result]  # return all the posts which belongs to a specific blog
