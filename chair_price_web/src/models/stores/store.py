
class Store:
    def __init__(self, name, url_prefix):
        self.name = name
        self.url_prefic = url_prefix


    def __repr__(self):
        return "<Store {}>".format(self.name)
