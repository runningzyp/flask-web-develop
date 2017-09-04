# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author  : 湛允鹏
# Link    :
from hello import db
from hello import User, Role
db.drop_all()
db.create_all()

admin_role = Role(name='Admin')
mod_roel = Role(name='Moderator')
user_role = Role(name='User')
user_john = User(username='john', role=admin_role)
user_susan = User(username='susan', role=user_role)
user_steve = User(username='steve', role=user_role)

db.session.add_all([admin_role, mod_roel, user_role,
                    user_john, user_susan, user_steve])

db.session.commit()

print(admin_role.id)
print(mod_roel.id)
print(user_role.id)

admin_role.name = 'Administrator'
db.session.add(admin_role)
db.session.commit()

db.session.delete(mod_roel)
db.session.commit()

print(Role.query.all())
print(Role.query.first())
print(User.query.all())
print(User.query.filter_by(role=user_role).all())
print(str(User.query.filter_by(role=user_role)))
print(str(User.query))