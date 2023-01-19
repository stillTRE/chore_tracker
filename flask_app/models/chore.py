from flask_app.config.mysqlconnection import connectToMySQL
db = "chore_tracker"
from flask import flash, session
from flask_app.models import household, user, member
from datetime import datetime
dateFormat = '%Y-%m-%d'
today = datetime.today()

class Chore:
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.points = data['points']
        self.due_date = data['due_date']
        self.status = data['status']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.household_id = data['household_id']
        self.member_id = data['member_id']
        self.completed_by = None

    @staticmethod
    def validate_create(request):
        is_valid = True
        if len(request['title']) < 1:
            flash('Please enter a title for the chore', 'choreError')
            is_valid = False
        elif len(request['title']) < 5:
            flash('Please provide a more detailed title', 'choreError')
            is_valid = False
        if len(request['description']) < 1:
            flash('Please describe the chore', 'choreError')
            is_valid = False
        elif len(request['description']) < 20:
            flash('Please give more detail so it can be done right!', 'choreError')
            is_valid = False
        if len(request['points']) < 1:
            flash('Please provide a points reward value', 'choreError')
            is_valid = False
        if len(request['due_date']) < 1:
            flash('Please enter a due date for this chore', 'choreError')
            is_valid = False
        elif datetime.strptime(request['due_date'], dateFormat) < today:
            flash('Due date cannot be in the past or same day', 'choreError')
            is_valid = False
        if len(request['member_id']) < 1:
            flash('Please assign to a household member', 'choreError')
            is_valid = False
        return is_valid
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO chores (title, description, points, due_date, household_id, member_id) VALUES (%(title)s, %(description)s, %(points)s, %(due_date)s, %(household_id)s, %(member_id)s);"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def update(cls,data):
        query = "UPDATE chores SET title = %(title)s, description = %(description)s, points = %(points)s, due_date = %(due_date)s, status = %(status)s, updated_at = NOW(), member_id = %(member_id)s, completed_by = %(completed_by)s WHERE id = %(chore_id)s;"
        return connectToMySQL(db).query_db(query, data)
    
    @classmethod
    def getChoreByHousehold(cls, data):
        query = """
            SELECT chores.id, title, chores.description, chores.points, due_date, status, chores.created_at, chores.updated_at, chores.household_id, chores.member_id, chores.completed_by,
            members.*, completer.*
            FROM households
            LEFT JOIN chores
            ON households.id = chores.household_id
            LEFT JOIN members
            ON members.id = chores.member_id
            LEFT JOIN members AS completer
            ON completer.id = chores.completed_by
            WHERE chores.id = %(chore_id)s
            """
        results = connectToMySQL(db).query_db(query, data)
        print(results)
        view_one = cls(results[0])
        view_one.completed_by = results[0]['completer.name']
        return view_one
    
    @classmethod
    def getAll(cls):
        query = """
            SELECT chores.id, title, chores.description, chores.points, due_date, status, chores.member_id, chores.created_at, chores.updated_at,
            households.id as household_id, family_name, location, households.description, households.created_at as uca, households.updated_at as uua,
            members.id, name, members.points, username, password, members.created_at, members.updated_at, members.household_id
            FROM chores
            JOIN households on households.id = chores.household_id
            JOIN members on members.id = chores.member_id;
            """
        chores_from_db = connectToMySQL(db).query_db(query)
        chores = []
        for chore in chores_from_db:
            chore_object = cls(chore)
            chore_object.household = household.Household( 
                {
                    "id": chore["household_id"],
                    "family_name": chore["family_name"],
                    "location": chore["location"],
                    "description": chore["description"],
                    "created_at": chore["uca"],
                    "updated_at": chore["uua"]
                }
            )
            chore_object.member = member.Member(
                {
                    'id' : chore['id'],
                    'name' : chore['name'],
                    'points' : chore['points'],
                    'username' : chore['username'],
                    'password' : None,
                    'created_at' : chore['created_at'],
                    'updated_at' : chore['updated_at'],
                    'household_id' : chore['household_id']
                }
            )
            chores.append(chore_object)
            print(chores[0])
        return chores

    @classmethod
    def choreComplete(cls):
        if 'user_id' in session:
            Chore.completed_by = session['user_id']
        elif 'member_id' in session:
            Chore.completed_by = session['member_id']
        return Chore.completed_by

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM chores WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)
    
    @classmethod
    def review(cls, data):
        query = "UPDATE chores SET status = 'Needs Review' WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)
    
    @classmethod
    def markComplete(cls, data):
        query = "UPDATE chores SET status = 'Completed' WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)