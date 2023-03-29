from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models import user, recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/recipes")
def dashboard():
    data = {"email" : session["user_email"]}
    user_display = user.User.get_by_email(data)
    recipes = recipe.Recipe.get_all()
    return render_template("dashboard.html", user = user_display, recipes = recipes)

@app.route("/register", methods = ["POST"])
def register():
    if not user.User.validate_registration(request.form):
        return redirect("/")

    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "password" : pw_hash
    }
    user.User.new_user(data)
    session["user_email"] = data["email"]
    return redirect("/recipes")

@app.route("/login", methods = ["POST"])
def login():
    data = { "email" : request.form["email"]}
    user_check = user.User.get_by_email(data)
    if user_check == False:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_check.password, request.form["password"]):
        flash("Invalid Email/Password")
        return redirect("/")
    session["user_email"] = data["email"]
    return redirect("/recipes")

@app.route("/logout", methods = ["POST"])
def logout():
    session.clear()
    return redirect("/")