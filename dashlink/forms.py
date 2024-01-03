from flask_wtf import FlaskForm
# from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, URLField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from dashlink.models import User
from flask_login import current_user


# Contact/Feedback Form
class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    feedback = TextAreaField('Feedback', validators=[DataRequired(), Length(min=0, max=50)])
    submit = SubmitField('Send')


# Register/Signup Form
class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email address', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Signup')

    # Cheking for duplicates
    def validate_username(self, username):
        duplicate = User.query.filter_by(username=username.data).first()
        if duplicate:
            raise ValidationError('Username already taken')
        
    def validate_email(self, email):
        duplicate = User.query.filter_by(email=email.data).first()
        if duplicate:
            raise ValidationError('This email is already used by another account')



# Login Form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    # rememberme = BooleanField('Remember me') # Not Useful now... Due to debugging process (only me can understand LOL)
    submit = SubmitField('Login')



# Edit User account settings form
class EditAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Save')

    # Cheking for duplicates
    def validate_username(self, username):
        if username.data != current_user.username:
            duplicate = User.query.filter_by(username=username.data).first()
            if duplicate:
                raise ValidationError('Username already taken')
        
    def validate_email(self, email):
        if email.data != current_user.email:
            duplicate = User.query.filter_by(email=email.data).first()
            if duplicate:
                raise ValidationError('This email is already used by another account')



# Dash URL Form
class AddURLForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=3, max=15)])
    long_url = URLField('Original link', validators=[DataRequired()])
    desc = TextAreaField('Note (Optional)', validators=[Length(min=0, max=50)])
    submit = SubmitField('Add')


# Edit Dashed URL Form
class EditURLForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=3, max=15)])
    long_url = URLField('Original link', validators=[DataRequired()])
    short_url = StringField('DashLink', validators=[DataRequired(), Length(min=3, max=20)])
    desc = TextAreaField('Note (Optional)', validators=[Length(min=0, max=50)])
    submit = SubmitField('Save')