from flask_restful import Resource
from flask import jsonify

from app import flask_app, setJSONFormat
from models.user import User
from models.group import Group
from sqlalchemy import func, desc, asc
from db import db

class UserApi(Resource):
    def get(self, user_id):
        setJSONFormat()
        try:
            return jsonify(User.query.order_by(User.name).filter(User.id == user_id).first())
        except Exception as e:
            return jsonify(message="Error : %s" % e)

    def delete(self, user_id):
        setJSONFormat()
        try:
            User.query.filter(User.id == user_id).delete()
            db.session.commit()
            return jsonify(message="Success to delete User with id: %s" %user_id)
        except Exception as e:
            return jsonify(message="Error : %s" %e)


class UsersApi(Resource):
    def get(self):
        setJSONFormat()
        try:
            return jsonify(users=User.query.order_by(User.name).all())
        except Exception as e:
            return jsonify(message="Error : %s" % e)

    def post(self):
        args = parser.parse_args()
        name = args['name']
        email = args['email']
        user = User(name)
        user.email = email
        db.session.add(user)
        setJSONFormat()
        try:
            db.session.commit()
            return jsonify(user)
        except Exception as e:
            return jsonify(message="Error : %s" % e)

    def put(self):
        args = parser.parse_args()
        id = args['id']
        name = args['name']
        email = args['email']
        type = args['type']

        user = User.query.filter(User.id == id).first()
        setJSONFormat()
        if user is None:
            if type == 'force':
                user = User(name)
                user.email = email
                db.session.add(user)
                try:
                    db.session.commit()
                    return jsonify(user)
                except Exception as e:
                    return jsonify(message="Error : %s" %e)
            return jsonify(messages='User with id: %s is not exists' % id)
        else:
            if name:
                user.name = name
            if email:
                user.email = email

            try:
                db.session.commit()
                return jsonify(user)
            except Exception as e:
                return jsonify(message="Error : %s" %e)


@flask_app.route('/users/groups')
def users_with_groups():
    result = db.session.query(User, func.array_to_string(func.array_agg(func.distinct(Group.name)), ',').label('group_name'), func.count(Group.id)).join('groups').group_by(User).order_by(desc(User.name)).all()
    setJSONFormat()
    return jsonify(result)

@flask_app.route('/users/group')
def users_with_group():
    result = db.session.query(User, func.count(Group.id).label('group_count')).join('groups').group_by(User).order_by(asc('group_count')).all()
    setJSONFormat()
    return jsonify(result)

@flask_app.route('/user/<int:user_id>/groups')
def groups_from_user(user_id):
    setJSONFormat()
    user = User.query.filter(User.id == user_id).first()
    return jsonify(user.groups)
