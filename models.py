"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
import datetime

DEFAULT_IMG = "https://filestore.community.support.microsoft.com/api/images/0ce956b2-9787-4756-a580-299568810730?upload=true"
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = "user"

    id = db.Column(db.Integer,
                primary_key=True,
                autoincrement=True
                )
    
    first_name = db.Column(db.String(10), nullable=False)
    last_name = db.Column(db.String(10), nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMG)
    posts = db.relationship('Post', backref="user")

class Post(db.Model):

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                primary_key=True,
                autoincrement=True
                )
    title = db.Column(db.Text, nullable=False, default="New Post")
    content= db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, 
                           nullable=False, 
                           default=datetime.datetime.now()
                           )
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('user.id'), 
                        nullable=False
                        )

class Tag(db.Model):

    __tablename__ = "tags"
    
    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True
                    )
    
    name = db.Column(db.String,
                     nullable=False
                     )
    
    posts = db.relationship('Post', secondary="post_tags", backref="tags")
    
class PostTag(db.Model):

    __tablename__ = 'post_tags'

    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id'),
                        primary_key=True,
                        nullable=False
                        )
    tag_id = db.Column(db.Integer, 
                       db.ForeignKey('tags.id'), 
                       primary_key=True,
                       nullable=False
                       )