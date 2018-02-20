#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request
from hashlib import md5
import os
import datetime

app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:////%s' % os.path.expanduser('~/hearing_screening.db'))
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    input_code = db.Column(db.String(128), nullable=False)
    passed_screening = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<User {} : {}>'.format(self.input_code, self.passed_screening)


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
        m5.update('pass' + str(input_code) + str(input_code))
        pass_code = m5.hexdigest()

        if output_code == pass_code:
            passed_screening = True
        else:
            passed_screening = False

        user = User(input_code=input_code, passed_screening=passed_screening)
        db.session.add(user)
        db.session.commit()
        return 'true'


if __name__ == '__main__':
    db.create_all()
