# from flask_sqlalchemy import SQLAlchemy
# from flask import request
# from models import User, Post

# db = SQLAlchemy()


# def connect_db(app):
#     db.app = app
#     db.init_app(app)
#     app_ctx = app.app_context()
#     app_ctx.push()
#     db.create_all()


# def get_all_usr():
#     return User.query.all()

# def get_usr(user_id):
#     return User.query.filter(User.id == user_id).all()

# def delete_usr(user_id):
#     User.query.filter_by(id=user_id).delete()
#     db.session.commit()

# def update_usr(user_id):
#     User.query.filter(User.id == user_id).update({
#         User.first_name : request.form['first_name'],
#         User.last_name : request.form['last_name'],
#         User.img_url : request.form['img_url']
#     })
#     db.session.commit()

# def add_usr():
#     first_name = request.form['first_name']
#     last_name = request.form['last_name']
#     img_url = request.form['img_url']

#     user = User(first_name=first_name, last_name=last_name, img_url=img_url)
#     db.session.add(user)
#     db.session.commit()

# def post_add(user_id):
#     title = request.form["title"]
#     content = request.form["content"]
    
#     post = Post(title=title, content=content, user_id=user_id)
#     db.session.add(post)
#     db.session.commit()

# def retrieve_post(post_id):
#     return Post.query.get_or_404(post_id)

# def post_update(post_id):
#     Post.query.filter(Post.id == post_id).update({
#         Post.title : request.form['title'],
#         Post.content : request.form['content']
#     })
#     db.session.commit()

# def post_delete(post_id):
#     Post.query.filter_by(id=post_id).delete()
#     db.session.commit()