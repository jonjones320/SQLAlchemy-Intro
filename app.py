"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User

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