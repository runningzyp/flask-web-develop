from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('keep me loggedd in')
    submit = SubmitField('Log In')


class ResetPassword(FlaskForm):
    password = PasswordField('新密码', validators=[Required()])


class RegistrationForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Length(1, 64),
                                          Email()])

    username = StringField('用户名', validators=[Required(), Length(
        1, 64), Regexp('^[A-Za-z][A-Za-z0-9.]*$', 0, '用户名只能是字母数字或点')])
    password = PasswordField(
        '密码', validators=[Required(), EqualTo('password2', message='密码必须相同')])
    password2 = PasswordField('重复密码', validators=[Required()])

    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已被使用')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已被使用')


class ChangePasswordForm(FlaskForm):
    oldpassword = PasswordField('旧密码', validators=[Required()])
    newpassword = PasswordField('新密码密码',
                                validators=[Required(), EqualTo('newpassword2',
                                                                message='密码必须相同')])
    newpassword2 = PasswordField('重复密码', validators=[Required()])
    submit = SubmitField('提交更改')
