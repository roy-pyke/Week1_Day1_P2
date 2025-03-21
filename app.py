from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import DataRequired, Email

app = Flask(__name__)
app.secret_key = '2003'

class MyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
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
        name = form.name.data
        email = form.email.data

        #TODO: 存放数据，检查用户名是否重复，发送邮件
        return "Thank you for registering"

    return render_template('register.html')



if __name__ == '__main__':
    app.run(debug=True, port=5003)
