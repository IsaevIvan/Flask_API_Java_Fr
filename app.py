from enum import unique

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Файл БД
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable = False)
    email = db.Column(db.String(100), nullable = False, unique = True)

    def __repr__(self):
        return f'<User{self.name}>'

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'email': self.email}


if __name__ == '__main__':
    app.run(debug=True)
