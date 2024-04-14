from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, DataRequired, ValidationError, Email
from market.models import User
# import random
# from flask import flash, redirect, url_for, session
# from flask_mail import Message
# from market import email_sender

email_otp = StringField(label='Email OTP:', validators=[DataRequired()])


class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username.')

    def validate_email_add(self, email_add_to_check):
        email = User.query.filter_by(email_add=email_add_to_check.data).first()
        if email:
            raise ValidationError('This email already exists! Please try a different email address.')

    username = StringField(label='User Name:', validators=[Length(min=2, max=20), DataRequired()])
    email_add = StringField(label='Email Address:', validators=[DataRequired(), Email()])
    password1 = PasswordField(label='Create Password:', validators=[Length(min=5), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='CREATE ACCOUNT')

    # def submit(self):
    #     user = User.query.filter_by(username=self.username.data).first()
    #     if user:
    #         flash('Username already exists! Please try a different username.', category='danger')
    #     else:
    #         email = User.query.filter_by(email_add=self.email_add.data).first()
    #         if email:
    #             flash('This email already exists! Please try a different email address.', category='danger')
    #         else:
    #             # Generate and send OTP
    #             otp = str(random.randint(100000, 999999))
    #             msg = Message('OTP Verification', sender='sanikachoudhary22@gmail.com', recipients=[self.email_add.data])
    #             msg.body = f'Your OTP for registration is {otp}'
    #             email_sender.send(msg)
    #
    #             # Set OTP in session
    #             session['otp'] = otp
    #
    #             flash('OTP has been sent to your email. Please check and verify.', category='success')
    #             return redirect(url_for('verify_email'))


class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = StringField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')


class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase Stock!')


class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell Stock!')