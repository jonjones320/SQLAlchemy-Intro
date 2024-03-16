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

    def __repr__(self):
        s = self
        return f"<User id={s.id} first_name={s.first_namename} last_name={s.last_name} img_url={s.img_url}>" 

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

