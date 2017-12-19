from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, FileField, SelectField

from wtforms.validators import Required, Length, Email, Regexp
from ..models import Role


class EditProfileForm(FlaskForm):
    name = StringField('真实姓名', validators=[Length(0, 64)])
    location = StringField('住址', validators=[Length(0, 64)])
    avatar = FileField('头像')
    about_me = TextAreaField('关于我')
    submit = SubmitField('提交')


class EditProfileAdminForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Length(1, 64),
                                          Email()])

    username = StringField('用户名', validators=[Required(), Length(
        1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, '用户名只能是字母数字或点和下划线')])

    confirmed = BooleanField('已注册')
    role = SelectField('Role', coerce=int)
    name = StringField('真实姓名', validators=[Length(0, 64)])
    location = StringField('位置', validators=[Length(0, 64)])
    about_me = TextAreaField('关于我')

    submit = SubmitField('提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经注册')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已被使用')


class PostForm(FlaskForm):
    body = TextAreaField('在想什么呢? ', validators=[Required()])
    submit = SubmitField('发表')
