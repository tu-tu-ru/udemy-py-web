from flask import Flask, render_template, request, session, make_response

from src.common.database import Database
from src.models.blog import Blog
from src.models.post import Post
from src.models.user import User

app = Flask(__name__)
app.secret_key = "Bear"


@app.route('/')
def home_template():
    return render_template('home.html')


# 下边这个 @ 开头的是 define the routes
@app.route('/login')  # mysite.com/api/login
def login_template():
    return render_template("login.html")


@app.route('/register')
def register_template():
    return render_template("register.html")


@app.before_first_request
def initialize_database():
    Database.initialize()
    # TODO
    # Why?


@app.route('/auth/login', methods=['POST'])  # Only accept POST method at this point
def login_user():
    email = request.form['email']
    password = request.form['password']
    # 从 request 里获得输入框里的 email 和 password
    # email and password are the fields in the login.html
    # The web makes a request and send it to the application
    if User.login_valid(email, password):
        User.login(user_email=email)
        # 确认 email 和 password 可用后，给用户登陆
    else:
        session['email'] = None

    return render_template("profile.html", email=session['email'])
    # email=session['email'] 是要干嘛？
    # The profile.html page has the access to the session which contains THE email.


@app.route('/auth/register', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']
    # 把新用户输入的 email 和 password 保存给 User 对象的一个新的实例
    User.register(email, password)  # 注册新用户，其中有一个步骤是保存到 mongodb，最后把 email 赋值给 session 里的 email 的部分
    return render_template("profile.html", email=session['email'])


# user_id is assigned when I create a user
@app.route('/blogs/<string:user_id>')
@app.route('/blogs')
def user_blogs(user_id=None):
    if user_id is not None:
        # Find the user by pre-assigned id
        user = User.get_from_mongo_by_id(user_id)
    else:
        user = User.get_from_mongo_by_email(session['email'])

    # Find the blogs owned by this user
    blogs = user.get_blogs()

    return render_template("user_blogs.html", blogs=blogs, email=user.email, blog_id=user._id)


@app.route('/blogs/new', methods=['POST', 'GET'])
def create_new_blog():
    if request.method == 'GET':
        return render_template('new_blog.html')
    else:
        title = request.form['title']
        description = request.form['description']
        user = User.get_from_mongo_by_email(email=session['email'])  # 这里的 user 只是个 object

        new_blog = Blog(user.email, title, description, user._id)
        new_blog.save_to_mongo()

        return make_response(user_blogs(user._id))


# All post have a blog_id
@app.route('/posts/<string:blog_id>')
def blog_post(blog_id):
    blog = Blog.from_mongo(blog_id)
    posts = blog.get_posts()

    return render_template("posts.html", posts=posts, blog_title=blog.title, blog_id=blog._id)


@app.route('/posts/new/<string:blog_id>', methods=['POST', 'GET'])
def create_new_post(blog_id):  # The parameter `blog_id` comes from the URL above.
    if request.method == 'GET':
        return render_template("new_post.html", blog_id=blog_id)
    else:
        title = request.form['title']
        content = request.form['content']
        # author = request.form['author']

        user = User.get_from_mongo_by_email(email=session['email'])

        new_post = Post(blog_id=blog_id, title=title, content=content, author=user.email)
        new_post.save_to_mongo()

        return make_response(blog_post(blog_id))


if __name__ == "__main__":
    app.run()

