from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login import login_required, current_user
from Flask_Class import db
from Flask_Class.models import Post
from Flask_Class.posts.forms import PostForm

posts = Blueprint('posts', __name__)

@posts.route('/posts', methods=['GET'])
def all_posts():
    title = 'Posts'
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('posts.html', title = title, posts = posts)


@posts.route('/post/create', methods=['GET', 'POST'])
@login_required
def create_post():
    title = 'Create Post'
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title = form.title.data,
            content = form.content.data,
            description = form.description.data,
            author = current_user
        )
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.index'))
    return render_template('create_posts.html', title = title, form = form)


@posts.route('/post/<int:update_id>', methods=['GET', 'POST'])
@login_required
def update_post(update_id):
    post = db.get_or_404(Post, update_id)
    if post.author != current_user:
      abort(403)
    form = PostForm()
    title = "Update Post"
    if form.validate_on_submit():
        post.title = form.title.data
        post.description = form.description.data
        post.content = form.content.data

        db.session.commit()
        flash('Your post has been updated', 'success')
        return redirect(url_for('main.index'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.description.data = post.description
        form.content.data = post.content
    return render_template('update_posts.html', title = title, post= post, form = form)