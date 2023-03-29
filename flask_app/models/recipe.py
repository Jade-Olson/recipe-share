from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.under_mins = data["under_mins"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.date_made = data["date_made"]

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes JOIN users ON user_id = users.id"
        return connectToMySQL("recipes").query_db(query)

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM recipes JOIN users ON user_id = users.id WHERE recipes.id = %(id)s"
        result = connectToMySQL("recipes").query_db(query, data)
        return result[0]
    
    @classmethod
    def new_recipe(cls, data):
        query = "INSERT INTO recipes (name, under_mins, description, instructions, date_made, created_at, updated_at, user_id) VALUES (%(name)s, %(under_mins)s, %(description)s, %(instructions)s, %(date_made)s, NOW(), NOW(), %(user_id)s)"
        return connectToMySQL("recipes").query_db(query, data)

    @classmethod
    def update_recipe(cls,data):
        query = "UPDATE recipes SET name = %(name)s, under_mins = %(under_mins)s, date_made = %(date_made)s, description = %(description)s, instructions = %(instructions)s, updated_at = NOW() WHERE id = %(id)s"
        return connectToMySQL("recipes").query_db(query, data)

    @classmethod
    def delete_recipe(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s"
        return connectToMySQL("recipes").query_db(query,data)

    @staticmethod
    def validate_recipe(data):
        is_valid = True
        if len(data["name"]) < 1:
            flash("Name must not be blank")
            is_valid = False
        if len(data["description"]) < 1:
            flash("Description must not be blank")
            is_valid = False
        if len(data["instructions"]) < 1:
            flash("Instructions must not be blank")
            is_valid = False
        if len(data["date_made"]) < 1:
            flash("Date must not be blank")
            is_valid = False
        return is_valid