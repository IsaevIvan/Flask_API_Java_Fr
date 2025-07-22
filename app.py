from enum import unique

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Файл БД
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable = False)
    email = db.Column(db.String(100), nullable = False, unique = True)

    def __repr__(self):
        return f'<User{self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }

with app.app_context():
    db.create_all()

@app.route('/users', methods = ['GET'])
def get_users():
    users = User.query.all()
    users_list = [user.to_dict() for user in users]
    return jsonify(users_list)

@app.route('/users/<int:id>', methods = ['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'Error' : 'User not found'}), 404
    return jsonify(user.to_dict)


@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()

    if not data or 'name' not in data or 'email' not in data:
        return jsonify({'Error': 'Name and email are required!'}), 400

    new_user = User(name=data['name'], email=data['email'])

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User added!', 'user': new_user.to_dict()}), 201


if __name__ == '__main__':
    app.run(debug=True)
