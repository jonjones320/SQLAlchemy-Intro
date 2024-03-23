"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
import datetime

from flask import request

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)
    app_ctx = app.app_context()
    app_ctx.push()
    db.create_all()


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    first_name = db.Column(db.String(31),
                    nullable=False,
                    unique=False)
    last_name = db.Column(db.String(50),
                    nullable=True,
                    unique=True)
    img_url = db.Column(db.String(500), 
                    nullable=False,
                    default='https://images.unsplash.com/photo-1526800544336-d04f0cbfd700?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D')
    posts = db.Column(db.Text,
                    db.ForeignKey('post.id'),
                    nullable=False,
                    default='Start blogging today!')

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    def __repr__(self):
        s = self
        return f"<User id={s.id} first_name={s.first_name} last_name={s.last_name} img_url={s.img_url} posts={s.posts}>" 



class Post(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    title = db.Column(db.String(39),
                    nullable=False,
                    unique=True)
    content = db.Column(db.String(999),
                    nullable=False,
                    unique=True)
    user_id = db.Column(db.Integer,
                    db.ForeignKey('users.id'))
    # created_at = db.Column(db.String,
    #                 default="1999-12-31")

    # user = db.relationship('User', backref = 'post')

    def __repr__(self):
        s = self
        return f"<Post id={s.id} title={s.title} content={s.content} created_at={s.created_at} FK_User{s.user_id}>"
    


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String(51),
                    nullable=False,
                    unique=True)
    
    posts = db.relationship("Post", secondary="post_tags", backref="tags")

    def __repr__(self):
        s = self
        return f"<Tag id={s.id} tag={s.name}>" 
    


class PostTag(db.Model):
    __tablename__ = 'post_tags'

    post_id = db.Column(db.Integer,
                   db.ForeignKey('tags.id'),
                   primary_key=True,
                   unique = True)
    tag_id = db.Column(db.Integer,
                   db.ForeignKey('posts.id'),
                   primary_key=True,
                   unique = True)

####################################### Functions ####################################################

def get_all_usr():
    return User.query.all()

def get_usr(user_id):
    return User.query.get_or_404(user_id)

def delete_usr(user_id):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()

def update_usr(user_id):
    User.query.filter(User.id == user_id).update({
        User.first_name : request.form['first_name'],
        User.last_name : request.form['last_name'],
        User.img_url : request.form['img_url']
    })
    db.session.commit()

def add_usr():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    img_url = request.form['img_url']

    user = User(first_name=first_name, last_name=last_name, img_url=img_url)
    db.session.add(user)
    db.session.commit()

############# POSTS ###################

def get_all_posts():
    return Post.query.all()

def retrieve_post(post_id):
    return Post.query.get_or_404(post_id)

def post_add(user_id):
    title = request.form["title"]
    content = request.form["content"]
    # created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    # , created_at=created_at

    post = Post(title=title, content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()


def post_update(post_id):
    Post.query.filter(Post.id == post_id).update({
        Post.title : request.form['title'],
        Post.content : request.form['content']
    })
    db.session.commit()

def post_delete(post_id):
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    
####################### TAGS ###############################

def get_all_tags():
    return Tag.query.all()

def get_tag(tag_id):
    return Post.query.get_or_404(tag_id)

def tag_add():
    name = request.form["name"]

    tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit()

def tag_update(tag_id):
    Tag.query.filter(Tag.id == tag_id).update({
        Tag.name : request.form['name']
    })
    db.session.commit()

def tag_delete(tag_id):
    Post.query.filter_by(id=tag_id).delete()
    db.session.commit()
