import random

from flask import Blueprint, render_template, request

from app import MyForm, User, db, app

dbcontrol = Blueprint('dbcontrol', __name__)

@dbcontrol.route('/get_users')
def get_users():
    users = User.query.all()
    return '<br>'.join([f'{user.id}: {user.username} ({user.email})' for user in users])

@dbcontrol.route('/update_user/<int:user_id>', methods=['POST'])
def update_user(user_id):
    user = User.query.get(user_id)
    if user:
        user.username = request.form['username']
        db.session.commit()
        return 'updated'

    return 'not found'

@dbcontrol.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return 'deleted'

    return 'not found'