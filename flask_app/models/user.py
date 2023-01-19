from flask_app.config.mysqlconnection import connectToMySQL
db = "chore_tracker"
from flask import flash
from datetime import datetime
dateFormat = '%Y-%m-%d'
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PW_REGEX = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$")


class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.household = None

    @staticmethod
    def validate_create(request):
        is_valid = True
        if len(request['first_name']) < 1:
            flash('Please enter a first name', 'regError')
            is_valid = False
        elif len(request['first_name']) < 3:
            flash('First name must be longer than two characters', 'regError')
            is_valid = False
        if len(request['last_name']) < 1:
            flash('Please enter a last name', 'regError')
            is_valid = False
        elif len(request['last_name']) < 3:
            flash('Last name must be longer than two characters', 'regError')
            is_valid = False
        if len(request['email']) < 1:
            flash('Please enter an email address', 'regError')
            is_valid = False
        elif not EMAIL_REGEX.match(request['email']):
            flash('Invalid email address', 'regError')
            is_valid = False
        if User.getByEmail(request) != False:
            flash("Email is already registered", 'regError')
            is_valid = False
        if len(request['password']) < 1:
            flash('Please enter a password', 'regError')
            is_valid = False
        elif not PW_REGEX.match(request['password']):
            flash('Password must be at least 8 characters and contain at least one: Uppercase letter, lowercase letter, and number', 'regError')
            is_valid = False
        if len(request['passConf']) < 1:
            flash('Please confirm your password', 'regError')
            is_valid = False
        elif  request['password'] != request['passConf']:
            flash('Passwords do not match', 'regError')
            is_valid = False
        return is_valid

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def getAll(cls):
        query = "SELECT * FROM users;"
        users_from_db = connectToMySQL(db).query_db(query)
        users = []
        for user in users_from_db:
            users.append(cls(user))
        return users

    @classmethod
    def getById(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s";
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def update(cls,data):
        query = "UPDATE users SET first_name = %(first_name)s,last_name = %(last_name)s,email = %(email)s,updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def getByEmail(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    # @classmethod
    # def getHousehold(cls, data):
    #     query = """
    #         SELECT households.id as household_id, family_name, location, description, user_id
    #         FROM households
    #         LEFT JOIN users on households.user_id = users.id
    #         WHERE users.id = %(id)s; 
    #         """
    #     results = connectToMySQL(db).query_db(query, data)
    #     print(results)
    #     one_user = cls(results[0])
    #     one_user.household = results[0]['household_id']
    #     print(one_user.household)
    #     return cls(one_user[0])