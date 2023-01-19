from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models import member, household, chore
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from datetime import datetime
dateFormat = "%m/%d/%Y %I:%M %p"

@app.route('/member')
def memberLoginReg():
    return render_template('memberReg.html')

@app.route('/member/register', methods=['POST'])
def memberRegister():
    if member.Member.validate_create(request.form):
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data = {
            'household_id' : request.form['household_id'],
            'name': request.form['name'],
            'username': request.form['username'],
            'password': pw_hash
        }
        session['member_id'] = member.Member.save(data)
        session['household_id'] = request.form['household_id']
        return redirect('/member/home')
    return redirect('/member')

@app.route('/member/login', methods=['POST'])
def memberLogin():
    data = { "username" : request.form['username']}
    member_in_db = member.Member.getByUsername(data)
    if member_in_db:
        if bcrypt.check_password_hash(member_in_db.password, request.form['password']):
            session['member_id'] = member_in_db.id
            session['household_id'] = member_in_db.household_id
            return redirect('/member/home')
    flash("Invalid Email/Password", 'loginError')
    return redirect('/member')

@app.route('/member/home')
def memberDashboard():
    if 'member_id' not in session:
        return redirect('/member')
    return render_template('memberDashboard.html',  current_member = member.Member.getById({'id' : session['member_id']}), household = household.Household.getHouseholdByMember({'household_id' : session['household_id']}), all_chores = chore.Chore.getAll())

@app.route('/member/logout')
def memberLogout():
    session.clear()
    return redirect('/member')