#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request
from hashlib import md5

from hearing_screening import app
from hearing_screening import db
from hearing_screening.models import User

@app.route("/")
def root():
    return app.send_static_file('index.html')


@app.route("/save", methods=['POST', 'GET'])
def save():
    print('save')
    if request.method == 'POST':
        input_code = request.form["inputCode"]
        output_code = request.form["outputCode"]
        m5 = md5()
        m5.update(('pass' + str(input_code) + str(input_code)).encode())
        pass_code = m5.hexdigest()

        if output_code == pass_code:
            passed_screening = True
        else:
            passed_screening = False

        user = User(input_code=input_code, passed_screening=passed_screening)
        db.session.add(user)
        db.session.commit()
        return 'true'

