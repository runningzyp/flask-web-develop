from flask import render_template, request, redirect, url_for, flash
from . import auth
from flask_login import login_user, current_user
from flask_login import logout_user, login_required
from ..models import User
from . forms import LoginForm
from .forms import RegistrationForm
from .forms import ChangePasswordForm
from .forms import ResetPassword
from .. import db
from ..email import send_email
from flask import current_app


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user is None:
            flash('该账号还没有注册,请先注册')
            return render_template('auth/login.html', form=form)

        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next')or url_for('main.index'))
        flash('Invaild user name or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You hava logged outk')
    return redirect(url_for('main.index'))


'''
@auth.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = ResetPassword()
    if form.validate_on_submit():
        user=user.query.filter_by(email=form.email.data).first
'''


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.email.data == current_app.config['FLASKY_ADMIN']:
            flash('该账号已被使用')
            return render_template('auth/login.html', form=form)
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmtion_token()
        send_email(user.email, 'confirm your account', 'auth/email/confirm',
                   user=user, token=token)

        flash('我们已经发送了注册邮件，请按照提示操作')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')  # 确认路由
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('你已经完成了注册，谢谢')
    else:
        flash('错误')
    return redirect(url_for('main.index'))


@auth.route('/confirm')  # 重新确认路由
@login_required
def resend_confirm():
    token = current_user.generate_confirmtion_token()
    send_email(current_user.email, 'confirm your account', 'auth/email/confirm',
               user=current_user, token=token)

    flash('我们已经重新发送了认证邮件')

    return redirect(url_for('main.index'))

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint[:5] != 'auth.' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.oldpassword.data):
            current_user.password = form.newpassword.data
            db.session.add(current_user)
            flash('更改密码成功')
            return redirect(url_for('main.index'))
        else:
            flash('密码输入错误')
    return render_template('auth/change-password.html', form=form)
