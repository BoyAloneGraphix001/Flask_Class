from flask import Blueprint,render_template
from Flask_Class.models import Post

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
@main.route('/index', methods=['GET'])
def index():
    title = "Home Page"
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('index.html', title=title, posts = posts)

@main.route('/about', methods=['GET'])
def about():
    title = "About Page"
    return render_template('about.html', title=title)

