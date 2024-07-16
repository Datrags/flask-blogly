"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secret"

with app.app_context():
    connect_db(app)
    db.create_all()

@app.route("/")
def home_page():
    return redirect("/users")

@app.route("/users")
def user_list():
    users = User.query.all()
    return render_template("list.html", users=users)

@app.route("/users/new", methods=["GET"])
def new_user():

    return render_template("newuser.html")

@app.route("/users/new", methods=["POST"])
def add_user():
    user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['img_url'] or None
    )
    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:id>")
def user_page(id: int ):
    user = User.query.get_or_404(id)
    return render_template("user_page.html", user=user)

@app.route("/users/<int:id>/edit")
def edit_user_page(id: int):
    user = User.query.get_or_404(id) 
    return render_template("edit_user.html", user=user)

@app.route("/users/<int:id>/edit", methods=["POST"])
def post_user(id):
    user = User.query.get_or_404(id) 
    user.first_name = request.form['first_name']
    user.last_name=request.form['last_name']
    user.image_url=request.form['img_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:id>/delete", methods=["POST"])
def delete_user(id):
    user = User.query.get_or_404(id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/")