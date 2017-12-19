from flask import Flask, render_template, flash, redirect, url_for, request, abort
from flask import current_app

from flask_login import current_user, logout_user, login_required
from ..models import User, Role, Permission, Post
from ..decorator import admin_required
from . import main


from .forms import EditProfileForm, EditProfileAdminForm, PostForm
from .. import db
import os
UPLOAD_FOLDER = os.getcwd() + "/app/static/avatar/"


@main.route('/', methods=['POST', 'GET'])
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        post = Post(body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', form=form, posts=posts)


@main.route('/user/<username>')  # 用户资料路由
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=user, posts=posts)


@main.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        flash('ok')
    return render_template('upload.html')


@main.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        if request.method == 'POST':
            avatar = request.files['avatar']
            filename = current_user.username + \
                '.' + avatar.filename.split('.')[-1]
            if filename != current_user.username + '.':
                if os.path.exists(os.path.join(UPLOAD_FOLDER, filename)):
                    os.remove(os.path.join(UPLOAD_FOLDER, filename))

                avatar.save(os.path.join(UPLOAD_FOLDER, filename))
                current_user.real_avatar = '/static/avatar/' + filename
            # os.path.join(“home”, "me", "mywork")->“home/me/mywork"
        db.session.add(current_user)
        flash('修改信息成功')
        return redirect(url_for('main.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.adout_me = form.about_me.data
        db.session.add(user)
        flash('信息已更改')
        return redirect(url_for("main.user", username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.da = user.confirmed
    form.role.data = user.role
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)
