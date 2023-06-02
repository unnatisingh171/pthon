from flask_wtf import FlaskForm
from wtforms.fields import DateField
from wtforms import StringField,PasswordField,SubmitField ,validators
from wtforms.validators import Length,EqualTo,InputRequired,Email,ValidationError
from app.models import Employee
from flask_login import current_user
class RegisterForm(FlaskForm):
    def validate_email(self,email_to_check):
        if not current_user.is_authenticated:
            email_check=Employee.query.filter_by(email=email_to_check.data).first()
            if email_check:
                raise ValidationError('Email already exists! Please try to login')
    first_name=StringField(label='First Name',validators=[InputRequired()])
    last_name=StringField(label='Last Name',validators=[InputRequired()])
    email=StringField(label='Email',validators=[Email(), InputRequired()])
    password=PasswordField(label='Password',validators=[Length(min=4),InputRequired()])
    confirmed_password=PasswordField(label='Comfirm Password',validators=[EqualTo('password'),InputRequired()])
    dob=DateField('DOB', format='%Y-%m-%d',validators=(validators.DataRequired(),))
    phone_no=StringField(label='Phone Number',validators=[InputRequired(),Length(min=10)])
    address=StringField(label='Address',validators=[InputRequired()])
    submit_field=SubmitField(label='Submit')

class UpdateForm(FlaskForm):
    first_name=StringField(label='First Name',validators=[InputRequired()])
    last_name=StringField(label='Last Name',validators=[InputRequired()])
    email=StringField(label='Email')
    dob=DateField('DOB', format='%Y-%m-%d',validators=(validators.DataRequired(),))
    phone_no=StringField(label='Phone Number',validators=[InputRequired(),Length(min=10)])
    address=StringField(label='Address',validators=[InputRequired()])
    submit_field=SubmitField(label='Submit')

class LoginForm(FlaskForm):
    email=StringField(label='Email',validators=[Email(), InputRequired()])
    password=PasswordField(label='Password',validators=[Length(min=4),InputRequired()])
    submit_field=SubmitField(label='Submit')

class SearchForm(FlaskForm):
    search=StringField(label='search',validators=[InputRequired()])
    submit_field=SubmitField(label='Search')