from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models import household, user
from datetime import datetime
import uuid
dateFormat = "%m/%d/%Y %I:%M %p"

@app.route('/household')
def createHousehold():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('householdCreate.html', current_user = user.User.getById({'id' : session['user_id']}))

@app.route('/household/add', methods=['POST'])
def addHousehold():
    if 'user_id' not in session:
        return redirect("/")
    if household.Household.validate_create(request.form):
        data = {
            'id' : uuid.uuid4(),
            'family_name': request.form['family_name'],
            'location': request.form['location'],
            'description': request.form['description'],
            'user_id': session['user_id']
        }
        household.Household.save(data)
        return redirect('/user/home')
    return redirect('/household')

@app.route('/household/edit/<int:user_id>')
def editHousehold(user_id):
    if 'user_id' not in session:
        return redirect("/")
    return render_template('householdUpdate.html', current_user = user.User.getById({'id' : session['user_id']}),  household = household.Household.getHousehold({'id' : session['user_id']}))

@app.route('/household/update', methods=['POST'])
def updateHousehold():
    if 'user_id' not in session:
        return redirect("/")
    if household.Household.validate_create(request.form):
        data = {
            'family_name' : request.form['family_name'],
            'location' : request.form['location'],
            'description' : request.form['description'],
            'user_id' : session['user_id']
        }
        household.Household.update(data)
        return redirect('/user/home')
    return redirect(f"/household/edit/{session['user_id']}")

