from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models import user, household, chore, member
from datetime import datetime
dateFormat = "%m/%d/%Y %I:%M %p"

@app.route('/user/home')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')    
    return render_template('dashboard.html', current_user = user.User.getById({'id' : session['user_id']}), household = household.Household.getHousehold({'id' : session['user_id']}), all_chores = chore.Chore.getAll(), all_members = member.Member.getAllMembersByHHID())
