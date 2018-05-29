# To connect to a database
import pymongo


class Database:
    uri = "mongodb://127.0.0.1:27017" # uri is a static property
    DATABASE = None

    # get a client for me in mongodb
    # 下边的这个 statement 是告诉 python，这个静态的 def 没有 self 参数，因为它只被用在这个 class 里，不会有对应的 instance
    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.uri)  # uri lives in the database
        Database.DATABASE = client['stack']  # Database.DATABASE contains the client we just initialized

    # The database is added with new data by collection
    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)  # return a cursor back to mongodb

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

