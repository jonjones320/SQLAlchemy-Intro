"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)
    app_ctx = app.app_context()
    app_ctx.push()


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
    
    def __repr__(self):
        s = self
        return f"<User id={s.id} first_name={s.first_name} last_name={s.last_name} img_url={s.img_url}>" 


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

    user = db.relationship('User', backref = 'post')
    
    def __repr__(self):
        s = self
        return f"<Post id={s.id} title={s.title} content={s.content} created_at={s.created_at} FK_User{s.user_id}>"
    