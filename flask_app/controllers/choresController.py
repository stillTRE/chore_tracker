from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models import user, household, chore, member
from datetime import datetime
dateFormat = "%m/%d/%Y %I:%M %p"

@app.route('/chore')
def createChore():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('choreCreate.html', current_user = user.User.getById({'id' : session['user_id']}),  household = household.Household.getHousehold({'id' : session['user_id']}))

@app.route('/chore/add', methods=['POST'])
def addChore():
    if 'user_id' not in session:
        return redirect("/")
    if chore.Chore.validate_create(request.form):
        data = {
            'title': request.form['title'],
            'description': request.form['description'],
            'points': request.form['points'],
            'due_date' : request.form['due_date'],
            'household_id': request.form['household_id'],
            'member_id' : request.form['member_id']
        }
        chore.Chore.save(data)
        return redirect('/user/home')
    return redirect('/chore')

@app.route('/chore/edit/<int:chore_id>')
def editChore(chore_id):
    if 'user_id' not in session:
        return redirect('/')
    session['chore_id'] = chore_id
    return render_template('choreUpdate.html', current_user = user.User.getById({'id' : session['user_id']}), household = household.Household.getHousehold({'id' : session['user_id']}), chore = chore.Chore.getChoreByHousehold({'chore_id' : chore_id}))

@app.route('/chore/update', methods=['POST'])
def updateChore():
    if 'user_id' not in session:
        return redirect("/")
    if chore.Chore.validate_create(request.form):
        data = {
            'chore_id' : session['chore_id'],
            'title' : request.form['title'],
            'description' : request.form['description'],
            'points' : request.form['points'],
            'due_date' : request.form['due_date'],
            'status' : request.form['status'],
            'household_id' : request.form['household_id'],
            'member_id' : request.form['member_id'],
            'completed_by' : request.form['member_id']
        }
        if request.form['status'] == 'Completed':
            chore.Chore.choreComplete()
        chore.Chore.update(data)
        return redirect('/user/home')
    return redirect(f"/chore/edit/{session['chore_id']}")

@app.route('/chore/user/view/<int:chore_id>')
def viewChoreUser(chore_id):
    session['chore_id'] = chore_id
    if 'user_id' not in session:
        return redirect('/')
    return render_template('choreView.html', current_user = user.User.getById({'id' : session['user_id']}), chore = chore.Chore.getChoreByHousehold({'chore_id' : chore_id}))

@app.route('/chore/member/view/<int:chore_id>')
def viewChoreMember(chore_id):
    session['chore_id'] = chore_id
    if 'member_id' not in session:
        return redirect('/member')
    return render_template('choreView.html', current_member = member.Member.getById({'id' : session['member_id']}), chore = chore.Chore.getChoreByHousehold({'chore_id' : chore_id}))

@app.route('/chore/delete/<int:chore_id>')
def destroyChore(chore_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id" : chore_id
    }
    chore.Chore.destroy(data)
    return redirect('/user/home')

@app.route('/chore/review/<int:chore_id>')
def choreReview(chore_id):
    session['chore_id'] = chore_id
    if 'member_id' not in session:
        return redirect('/member')
    data = {
        "id" : chore_id
    }
    chore.Chore.review(data)
    return redirect('/member/home')

@app.route('/chore/complete/<int:chore_id>')
def choreCompleted(chore_id):
    session['chore_id'] = chore_id
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id" : chore_id
    }
    chore.Chore.markComplete(data)
    return redirect('/user/home')