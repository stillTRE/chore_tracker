from flask_app.config.mysqlconnection import connectToMySQL
db = "chore_tracker"
from flask import flash
from datetime import datetime
dateFormat = '%Y-%m-%d'
from flask_app.models import household
import re
PW_REGEX = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$")

class Member:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.points = data['points']
        self.username = data['username']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.household_id = data['household_id']

    @staticmethod
    def validate_create(request):
        is_valid = True
        if request['household_id'] != Member.getByHHid({'id' : request['household_id']}):
            flash("Invalid Household ID", 'regError')
            is_valid = False
        if len(request['name']) < 1:
            flash('Please enter your first name', 'regError')
            is_valid = False
        elif len(request['name']) < 3:
            flash('First name must be longer than two characters', 'regError')
            is_valid = False
        if len(request['username']) < 1:
            flash('Please enter a username', 'regError')
            is_valid = False
        elif len(request['username']) < 5:
            flash('Username must be longer than 4 characters', 'regError')
            is_valid = False
        if Member.getByUsername(request) != False:
            flash("Username is already registered", 'regError')
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
        query = "INSERT INTO members (household_id, name, username, password) VALUES (%(household_id)s, %(name)s, %(username)s, %(password)s);"
        return connectToMySQL(db).query_db(query,data)
    
    @classmethod
    def getByUsername(cls,data):
        query = "SELECT * FROM members WHERE username = %(username)s;"
        results = connectToMySQL(db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def getById(cls, data):
        query = "SELECT * FROM members WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])

    @classmethod 
    def getAllMembersByHHID(cls):
        query = """
            SELECT members.id, name, points, username, password, members.created_at, members.updated_at,
            households.id as household_id, family_name, location, households.description, households.created_at as uca, households.updated_at as uua
            from members
            JOIN households on households.id = members.household_id
            """
        members_from_db = connectToMySQL(db).query_db(query)
        members = []
        for member in members_from_db:
            member_object = cls(member)
            member_object.household = household.Household(
                {
                    "id": member["household_id"],
                    "family_name": member["family_name"],
                    "location": member["location"],
                    "description": member["description"],
                    "created_at": member["uca"],
                    "updated_at": member["uua"]
                }
            )
            members.append(member_object)
        return members


    @classmethod
    def getByHHid(cls, data):
        query = "SELECT id FROM households WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        print(results)
        if not results:
            return False
        return results[0]['id']
    

    # first stab at points redemption

    # @classmethod
    # def addPoints(cls):
    #     query = """
    #         SELECT chores.points, chores.status,
    #         members.points, members.id
    #         FROM chores
    #         JOIN members on chores.member_id = members.id
    #         WHERE chores.status = 'Completed'
    #         """
    #     results = connectToMySQL(db).query_db(query)
    #     if results.chores.status == 'Completed':
    #         results.members.points = results.members.points + results.chores.points
    #         return results