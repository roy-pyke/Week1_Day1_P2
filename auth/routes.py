import random

from flask import Blueprint, render_template, request

from app import MyForm, User, db, app

auth = Blueprint('auth', __name__)

@auth.route('/')
def index():
    form = MyForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        return f"name: {name}, email: {email}"
    return render_template('register.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = MyForm()
    if request.method == 'POST':
        if form.validate():
            name = form.name.data
            email = form.email.data

            # 生成不重复的8位数字ID
            random_id = random.randint(10**7, 10**8 - 1)
            while User.query.get(random_id):
                random_id = random.randint(10**7, 10**8 - 1)

            new_user = User(id=random_id, username=name, email=email)
            db.session.add(new_user)
            db.session.commit()

            return "Thank you for registering"

    return render_template('register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = MyForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data