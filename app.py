"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User, Post
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
app.debug = True
debug = DebugToolbarExtension(app)



@app.route("/")
def home():
    """Home"""
    return redirect("/users")


@app.route("/users")
def list_users():
    """Show all users"""
    users = User.query.all()
    return render_template("list-users.html", users=users)


@app.route("/users/new")
def create_user():
    """Create new user"""
    return render_template("new-user.html")


@app.route("/users/new", methods=["POST"])
def add_user():
    """Add new user"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    img_url = request.form['img_url']

    user = User(first_name=first_name, last_name=last_name, img_url=img_url)
    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>")
def view_user(user_id):
    """View user"""
    
    user = User.query.get_or_404(user_id)

    return render_template("view-user.html", user=user)


@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    """Edit a user"""
    user = User.query.get_or_404(user_id)

    return render_template("edit-user.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def update_user(user_id):
    """Post changes to edited user"""

    User.query.filter(User.id == user_id).update({
        User.first_name : request.form['first_name'],
        User.last_name : request.form['last_name'],
        User.img_url : request.form['img_url']
        })

    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Delete a user"""

    User.query.filter_by(id=user_id).delete()
    db.session.commit()

    return redirect("/users")

################################################################################################

@app.route("/users/[user-id]/posts/new")
def create_post(user_id):
    """Show form to add a post for that user"""
    user = User.query.filter(User.id == user_id).all()

    return render_template("create-post.html", user=user)


@app.route("/users/[user-id]/posts/new", methods=["POST"])
def add_post(user_id):
    """Handle create-post form; Add post and redirect to the user detail page"""
    title = request.form["title"]
    content = request.form["content"]
    created_at = db.Column(db.DateTime, server_default=datetime.datetime.utcnow)

    post = Post(title=title, content=content, created_at=created_at, user_id=user_id)
    db.session.add(post)
    db.session.commit()

    return redirect("/users/<int:user_id>")


@app.route("/posts/[post-id]")
def view_post(post_id):
    """Show a post. Show buttons to edit and delete the post"""

    post = Post.query.get_or_404(post_id)

    return render_template("view-post.html", post=post)


@app.route("/posts/[post-id]/edit")
def edit_post(post_id):
    """Show form to edit a post, and to cancel (back to user page)"""

    post = Post.query.get_or_404(post_id)

    return render_template("edit-post.html", post=post)


@app.route("/posts/[post-id]/edit", methods=["POST"])
def update_post():
    """Handle editing of a post. Redirect back to the post view"""

    return redirect("/posts/[post-id]")


@app.route("/posts/[post-id]/delete", methods=["POST"])
def delete_post():
    """Delete the post"""

    return redirect("/users")