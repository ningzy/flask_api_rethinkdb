import os
import rethinkdb as r
from jose import jwt
from datetime import datetime
from passlib.hash import pbkdf2_sha256

from flask import current_app

from api.utils.errors import ValidationError

conn = r.connect(db='papers')

class RethinkDBModel(object):
    pass

class User(RethinkDBModel):
    _table = 'users'

    @classmethod
    def create(cls, **kwargs):
        fullname = kwargs.get('fullname')
        email = kwargs.get('email')
        password = kwargs.get('password')
        password_conf = kwargs.get('password_conf')
        if password != password_conf:
            raise ValidationError("Pawssword and Confirm password doesn't match")
        password = cls.hash_password(password)
        doc = {
            'fullname': fullname,
            'email': email,
            'password': password,
            'date_created': datetime.now(r.maketimezone('+1:00')),
            'date_modified': datetime.now(r.maketimezone('+1:00'))
        }
        r.table(cls._table).insert(doc).run(conn)
    
    @classmethod
    def validate(cls, email, password):
        docs = list(r.table(cls._table).filter({'email': emial}).run(conn))

        if not len(docs):
            rais ValidationError("Could not find the e-mail address you specified")

        _hash = docs[0]['password']

        if cls.verify_password(password, _hash):
            try:
                token = jwt.encode({'id': docs[0]['id']}, current_app.config['SECRET_KEY'], algorithm='HS256')
                return token
            except JWTError:
                raise ValidationError("There was a problem while trying to create a JWT token.")
            else:
                raise ValidationError("The password you inputted was incorrect.")

    @staticmethod
    def hash_password(password):
        return pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)

    @staticmethod
    def verify_password(password, _hash):
        return pbkdf2_sha256.verify(password, _hash)

    