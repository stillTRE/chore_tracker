from flask_app.config.mysqlconnection import connectToMySQL
db = "chore_tracker"
from flask import flash
from flask_app.models import member
from datetime import datetime
dateFormat = '%Y-%m-%d'

class Household:
    def __init__(self,data):
        self.id = data['id']
        self.family_name = data['family_name']
        self.location = data['location']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.members = []

    @staticmethod
    def validate_create(request):
        is_valid = True
        if len(request['family_name']) < 1:
            flash('Please enter a family name', 'regError')
            is_valid = False
        elif len(request['family_name']) < 3:
            flash('Family name must be longer than two characters', 'regError')
            is_valid = False
        if len(request['location']) < 1:
            flash('Please enter the location of your household', 'regError')
            is_valid = False
        elif len(request['location']) < 3:
            flash('Household location must be longer than two characters', 'regError')
            is_valid = False
        if len(request['description']) < 1:
            flash('Please enter a description of your household', 'regError')
            is_valid = False
        elif len(request['description']) < 20:
            flash('Please describe your household, i.e amount of family members, lifestyle, etc.', 'regError')
            is_valid = False
        return is_valid
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO households (id, family_name, location, description, user_id) VALUES (%(id)s, %(family_name)s, %(location)s, %(description)s, %(user_id)s);"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def getHousehold(cls, data):
        query = """
            SELECT households.id AS id, family_name, location, description, households.created_at, households.updated_at, user_id
            FROM users
            LEFT JOIN households on households.user_id = users.id
            WHERE users.id = %(id)s; 
            """
        results = connectToMySQL(db).query_db(query, data)
        print(results)
        one_user = cls(results[0])
        print(one_user)
        one_user.results = results[0]['id']
        return one_user

    @classmethod
    def getHouseholdByMember(cls, data):
        query = """
            SELECT households.id AS id, family_name, location, description, households.created_at, households.updated_at
            FROM members
            LEFT JOIN households on members.household_id = households.id
            WHERE members.household_id = %(household_id)s;
            """
        results = connectToMySQL(db).query_db(query, data)
        print(results)
        one_member = cls(results[0])
        print(one_member)
        one_member.results = results[0]['id']
        return one_member
    
    @classmethod
    def getHouseholdWithMembers(cls, data):
        query = "SELECT * FROM households LEFT JOIN members ON households.id = members.household_id WHERE household.id = %(household_id)s;"
        results = connectToMySQL(db).query_db(query, data)

        household = cls(results[0])
        for row_from_db in results:
            member_data = {
                "id" : row_from_db["members.id"],
                "name" : row_from_db["members.name"],
                "points" : row_from_db["members.points"],
                "username" : row_from_db["members.username"],
                "password" : None,
                "created_at" : row_from_db["members.created_at"],
                "updated_at" : row_from_db["members.updated_at"],
            }
            household.members.append(member.Member(member_data))
            print(household)
        return household
    
    @classmethod
    def update(cls,data):
        query = "UPDATE households SET family_name = %(family_name)s, location = %(location)s, description = %(description)s, updated_at = NOW() WHERE user_id = %(user_id)s;"
        return connectToMySQL(db).query_db(query, data)
    