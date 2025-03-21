from flask import Flask, render_template, request
import random
from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import DataRequired, Email, length
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = '2003'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

with app.app_context():
    db.create_all()

class MyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), DataRequired(), length(min=2, max=30)])
    email = StringField('Email', validators=[DataRequired(), DataRequired(), Email()])
    submit = SubmitField('Submit')

@app.route('/')
def index():
    form = MyForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        return f"name: {name}, email: {email}"
    return render_template('register.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = MyForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data

@app.route('/get_users')
def get_users():
    users = User.query.all()
    return '<br>'.join([f'{user.id}: {user.username} ({user.email})' for user in users])

@app.route('/update_user/<int:user_id>', methods=['POST'])
def update_user(user_id):
    user = User.query.get(user_id)
    if user:
        user.username = request.form['username']
        db.session.commit()
        return 'updated'

    return 'not found'

@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return 'deleted'

    return 'not found'





if __name__ == '__main__':
    app.run(debug=True, port=5003)
