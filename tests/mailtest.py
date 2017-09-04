# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author  : 湛允鹏
# Link    :
# print(os.environ.get('MAIL_USERNAME'))
from flask_mail import Message
from hello import mail
msg = Message('test subject', sender='zhanyunpeng1996@163.com',
              recipients=['zhanyunpeng1996@163.com'])
msg.body = 'text body'
msg.html = '<b>HTML</b> body'
with app.app_context():
    mail.send(msg)
