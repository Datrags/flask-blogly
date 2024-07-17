"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User, Post

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
    """"Route leads to /user when on starting page"""
    return redirect("/users")

@app.route("/users")
def user_list():
    """List all users in database"""
    users = User.query.all()
    return render_template("list.html", users=users)

@app.route("/users/new", methods=["GET"])
def new_user():
    """Shows form for a new user"""
    return render_template("newuser.html")

@app.route("/users/new", methods=["POST"])
def add_user():
    """adds new user to database"""
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
    """shows user page based on user id"""
    user = User.query.get_or_404(id)
    posts = Post.query.filter(Post.user_id == user.id).all()
    return render_template("user_page.html", user=user, posts=posts)

@app.route("/users/<int:id>/edit", methods=["GET"])
def edit_user_page(id: int):
    """shows form to edit post"""
    user = User.query.get_or_404(id) 
    return render_template("edit_user.html", user=user)

@app.route("/users/<int:id>/edit", methods=["POST"])
def post_user(id):
    """updates user from form"""
    user = User.query.get_or_404(id) 
    user.first_name = request.form['first_name']
    user.last_name=request.form['last_name']
    user.image_url=request.form['img_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:id>/delete", methods=["POST"])
def delete_user(id):
    """deletes user from database"""
    user = User.query.get_or_404(id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/")

@app.route("/users/<int:id>/posts/new", methods=["GET"])
def new_user_post(id):
    """shows form to create a new post for user"""
    user = User.query.get_or_404(id)

    return render_template("post_form.html", user=user)

@app.route("/users/<int:id>/posts/new", methods=["POST"])
def handle_post(id):
    """handles input from new post form and creates post on database"""
    user = User.query.get_or_404(id)
    post = Post(
        title=request.form['title'],
        content=request.form['content'],
        user_id=id
    )
    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{user.id}")

@app.route("/posts/<int:id>")
def show_post(id):
    """shows post based on post's id"""
    post = Post.query.get_or_404(id)

    return render_template("post.html", post=post)

@app.route("/posts/<int:id>/edit", methods=["GET"])
def show_edit_post(id):
    """shows form to edit post"""
    post = Post.query.get_or_404(id)

    return render_template("edit_post.html", post=post)

@app.route("/posts/<int:id>/edit", methods=["POST"])
def handle_edit_post(id):
    """updates post in database based on form"""
    post = Post.query.get_or_404(id)
    post.title = request.form['title']
    post.content=request.form['content']

    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post.id}")

@app.route("/posts/<int:id>/delete", methods=["POST"])
def handle_post_edit(id):
    """deletes posts from database"""
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()

    return redirect("/")