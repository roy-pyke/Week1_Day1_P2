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

from auth.routes import auth
from dbcontrol.routes import dbcontrol

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(dbcontrol, url_prefix='/dbcontrol')

if __name__ == '__main__':
    app.run(debug=True, port=5003)
