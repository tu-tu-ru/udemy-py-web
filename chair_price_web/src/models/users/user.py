import uuid


class User:
    def __init__(self, email, password, _id):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex

    def __repr__(self):
        return "<User {}>".format(self.email)