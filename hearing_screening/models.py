#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hearing_screening import db

import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    input_code = db.Column(db.String(128), nullable=False)
    passed_screening = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<User {} : {}>'.format(self.input_code, self.passed_screening)
