#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Create the database structure (clearing it if it already exists) and insert the tests and conditions as
defined in the test configuration.

To run: ::

    $ python create_db.py

"""

from hearing_screening import db
db.drop_all()
db.create_all()