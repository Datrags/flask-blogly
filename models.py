"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

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
