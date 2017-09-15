from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required
from wtforms.validators import Required, Length


class EditProfileForm(FlaskForm):
    name = StringField('真实姓名', validators=[Length(0, 64)])
    location = StringField('住址', validators=[Length(0, 64)])
    about_me = TextAreaField('关于我')
    submit = SubmitField('提交')


class EditProfileAdminForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Length(1, 64),
                                          Email()])

    username = StringField('用户名', validators=[Required(), Length(
        1, 64), Regexp('^[A-Za-z][A-Za-z0-9.]*$', 0, '用户名只能是字母数字或点')])
