from flask_app.config.mySqlconnection import connectToMySQL
import re
from flask import flash
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class User:
    name_db = "login_and_registration"
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
    @classmethod
    def save(cls, data):
        query = "insert into users (first_name, last_name, email, password) values (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.name_db).query_db(query, data)
    @classmethod
    def get_by_email(cls,data):
        query = "select * from users where email = %(email)s;"
        result = connectToMySQL(cls.name_db).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])
    @classmethod
    def get_by_id(cls,data):
        query = "select * from users where id = %(id)s;"
        results = connectToMySQL(cls.name_db).query_db(query,data)
        print(results)
        return cls(results[0])
    @staticmethod
    def validate_registration(data):
        valid = True
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!")
            valid = False
        elif len(data["email"])< 1:
            flash("Please input an email.")
            valid = False
        if len(data["first_name"])<1 or len(data["last_name"])<1:
            flash("Please input a Proper name.")
            valid = False
        if len(data["password"])<8:
            flash("Invalid password, must be 8 characters or more")
            valid = False
        if not data["password"] == data["confirmPass"]:
            flash("passwords must match!")
            valid = False
        return valid