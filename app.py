"""Blogly application."""

from flask import Flask, render_template, redirect, url_for
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
app.debug = True
debug = DebugToolbarExtension(app)

connect_db(app)


@app.route("/")
def home():
    """Home"""
    return redirect("/users")

###########################################   USERS   #####################################################

@app.route("/users")
def list_users():
    """Show all users"""

    users = get_all_usr()
    
    return render_template("/user/list-users.html", users=users)


@app.route("/users/new")
def create_user():
    """Create new user"""
    
    return render_template("/user/new-user.html")


@app.route("/users/new", methods=["POST"])
def add_user():
    """Add new user"""

    add_usr()

    return redirect("/users")


@app.route("/users/<int:user_id>")
def view_user(user_id):
    """View user"""
    
    user = get_usr(user_id)

    return render_template("/user/view-user.html", user=user)


@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    """Edit a user"""

    user = get_usr(user_id)

    return render_template("/user/edit-user.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def update_user(user_id):
    """Post changes to edited user"""

    update_usr(user_id)

    return redirect("/users")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Delete a user"""

    delete_usr(user_id)

    return redirect("/users")

###########################################   POSTS   #####################################################

@app.route("/users/<int:user_id>/posts/new")
def create_post(user_id):
    """Add new post for a user"""
    
    user = get_usr(user_id)
    tags = get_all_tags()

    return render_template("/post/create-post.html", user=user, tags=tags)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_post(user_id):
    """Handle create-post form; Add post and redirect to the user detail page"""

    post_add(user_id)

    return redirect("/users")


@app.route("/posts/<int:post_id>")
def view_post(post_id):
    """Show a post. Show buttons to edit and delete the post"""

    post = retrieve_post(post_id)

    return render_template("/post/view-post.html", post=post)


@app.route("/posts/<int:post_id>/edit")
def edit_post(post_id):
    """Show form to edit a post, and to cancel (back to user page)"""

    post = retrieve_post(post_id)
    tags = get_all_tags()

    return render_template("/post/edit-post.html", post=post, tags=tags)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def update_post(post_id):
    """Handle editing of a post. Redirect back to the post view"""

    post_update(post_id)

    return redirect(url_for("view_post", post_id=post_id))


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Delete post"""

    post_delete(post_id)

    return redirect("/users")

############################################# Tags #########################################################

@app.route('/tags')
def list_tags():
    """Lists all tags, with links to the tag detail page."""

    tags = get_all_tags()

    return render_template("/tag/list_tags.html", tags=tags)


@app.route('/tags/<int:tag_id>')
def tag_details(tag_id):
    """View tag details. Have links to edit form and to delete."""

    tag = get_tag(tag_id)

    return render_template("/tag/view_tag.html", tag=tag)


@app.route('/tags/new')
def new_tag():
    """Shows a form to add a new tag."""

    return render_template("/tag/new_tag.html")


@app.route('/tags/new', methods=["POST"])
def add_tag():
    """Process add form, adds tag, and redirect to tag list"""

    tag_add()

    return redirect("/tags")


@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    """Show edit form for a tag"""

    tag = get_tag(tag_id)

    return render_template("/tag/edit_tag.html", tag=tag)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def update_tag(tag_id):
    """Process edit form, edit tag, and redirects to the tags list"""

    tag_update(tag_id)

    return redirect("/tags")


@app.route('/tags/<int:tag_id>/delete')
def delete_tag():
    """Delete tag"""

    tag_delete()

    return redirect("/tags")