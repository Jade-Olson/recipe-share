from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models import recipe, user

@app.route("/recipes/new")
def new_recipe_page():
    data = {"email" : session["user_email"]}
    user_display = user.User.get_by_email(data)
    return render_template("new.html", user = user_display)

@app.route("/recipes/new/submit", methods = ["POST"])
def new_recipe():
    userdata = {"email" : session["user_email"]}
    user_display = user.User.get_by_email(userdata)
    print(request.form["under_mins"])
    data = {
        "name" : request.form["name"],
        "under_mins" : request.form["under_mins"],
        "description" : request.form["description"],
        "instructions" : request.form["instructions"],
        "date_made" : request.form["date_made"],
        "user_id" : user_display.id
    }
    if not recipe.Recipe.validate_recipe(data):
        return redirect("/recipes/new")

    recipe.Recipe.new_recipe(data)
    return redirect("/recipes")

@app.route("/recipes/<id>")
def view_recipe(id):
    data = {"email" : session["user_email"]}
    user_display = user.User.get_by_email(data)
    data = {"id" : id}
    recipe_data = recipe.Recipe.get_one(data)
    print(recipe_data)
    return render_template("view.html", recipe = recipe_data, user = user_display)

@app.route("/recipes/<id>/update")
def update_recipe_page(id):
    data = {"email" : session["user_email"]}
    user_display = user.User.get_by_email(data)
    data = {"id" : id}
    recipe_data = recipe.Recipe.get_one(data)
    return render_template("edit.html", recipe = recipe_data, user = user_display)

@app.route("/recipes/<id>/update/submit", methods = ["POST"])
def update_recipe(id):
    data = {
        "name" : request.form["name"],
        "under_mins" : request.form["under_mins"],
        "description" : request.form["description"],
        "instructions" : request.form["instructions"],
        "date_made" : request.form["date_made"],
        "id" : id
    }
    if not recipe.Recipe.validate_recipe(data):
        return redirect(f"/recipes/{id}/update")
    recipe.Recipe.update_recipe(data)
    return redirect(f"/recipes/{id}")

@app.route("/recipes/<id>/delete")
def delete_recipe(id):
    data = {"id" : id}
    recipe.Recipe.delete_recipe(data)
    return redirect("/recipes")