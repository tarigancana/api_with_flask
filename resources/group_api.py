from flask_restful import Resource
from flask import jsonify

from app import flask_app, setJSONFormat
from models.group import Group
from models.user import User
from sqlalchemy import func, desc, asc
from db import db

class GroupsApi(Resource):
    def get(self):
        setJSONFormat()
        try:
            return jsonify(groups=Group.query.order_by(Group.name).all())
        except Exception as e:
            return jsonify(message="Error : %s" % e)

    def post(self):
        args = parser.parse_args()
        name = args['name']
        group = Group(name)
        db.session.add(group)
        setJSONFormat()
        try:
            db.session.commit()
            return jsonify(group)
        except Exception as e:
            return jsonify(message="Error : %s" % e)

    def put(self):
        args = parser.parse_args()
        id = args['id']
        name = args['name']
        type = args['type']

        group = Group.query.filter(Group.id == id).first()
        setJSONFormat()
        if group is None:
            if type == 'force':
                group = Group(name)
                db.session.add(group)
                try:
                    db.session.commit()
                    return jsonify(group)
                except Exception as e:
                    return jsonify(message="Error : %s" %e)
            return jsonify(messages='Group with id: %s is not exists' % id)
        else:
            if name:
                group.name = name
            try:
                db.session.commit()
                return jsonify(group)
            except Exception as e:
                return jsonify(message="Error : %s" %e)

class GroupApi(Resource):
    def get(self, group_id):
        setJSONFormat()
        try:
            return jsonify(Group.query.order_by(Group.name).filter(Group.id == group_id).first())
        except Exception as e:
            return jsonify(message="Error : %s" % e)

    def delete(self, group_id):
        setJSONFormat()
        try:
            group = Group.query.filter(Group.id == group_id).first()
            group.clear_group()
            Group.query.filter(Group.id == group_id).delete()
            db.session.commit()
            return jsonify(message="Success to delete Group with id: %s" %group_id)
        except Exception as e:
            return jsonify(message="Error : %s" %e)

class GroupModifyUserApi(Resource):
    def post(self, group_id,command,user_id):
        setJSONFormat()
        try:
            if command == 'add':
                group = Group.query.filter(Group.id == group_id).first()
                user = User.query.filter(User.id == user_id).first()
                if group is not None and user is not None:
                    group.users.append(user)
                    db.session.commit()
                    return jsonify(message= 'success add user %s' % user.name)
            elif command == 'del':
                group = Group.query.filter(Group.id == group_id).first()
                user = User.query.filter(User.id == user_id).first()
                if group is not None and user is not None:
                    group.users.remove(user)
                    db.session.commit()
                    return jsonify(message= 'success remove user %s from group' % user.name)
        except Exception as e:
            return jsonify(message="Error: %s" %e)


@flask_app.route('/group/users')
def group_with_users():
    result = db.session.query(Group, func.count('user_id').label('user_count')).join('users').group_by(Group).order_by(desc('user_count')).all()
    setJSONFormat()
    return jsonify(result)

@flask_app.route('/group/<int:group_id>/users')
def users_from_group(group_id):
    setJSONFormat()
    group = Group.query.filter(Group.id == group_id).first()
    return jsonify(group.users.all())

