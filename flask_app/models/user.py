from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]

    @classmethod
    def new_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL("recipes").query_db(query, data)

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("recipes").query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def validate_registration(data):
        is_valid = True
        user_in_db = User.get_by_email(data)
        if len(data["first_name"]) < 1:
            flash("First Name is required.")
            is_valid = False
        if len(data["last_name"]) < 1:
            flash("Last Name is required.")
            is_valid = False
        if not EMAIL_REGEX.match(data["email"]):
            flash("Email address is invalid.")
            is_valid = False
        if user_in_db:
            flash("Email already in use.")
            is_valid = False
        if len(data["password"]) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False
        if data["password"] != data["confirm_password"]:
            flash("Passwords do not match.")
            is_valid = False
        return is_valid
            