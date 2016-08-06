from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse, abort
from flask_sqlalchemy import SQLAlchemy
from flask.json import JSONEncoder
from sqlalchemy import text
import json
import os

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class FlaskApiEncoder(JSONEncoder):
    item_separator = ','
    key_seoarator  = ':'
    def default(self, obj):
        if isinstance(obj, User):
            return {
                'id': obj.id,
                'name': obj.name,
                'email': obj.email
            }
        elif isinstance(obj, Group):
            return {
                'id': obj.id,
                'name': obj.name,
            }
        return super(FlaskApiEncoder, self).default(obj)

app.json_encoder = FlaskApiEncoder

db = SQLAlchemy(app)
from models.user import User
from models.group import Group

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('id', type=str)
parser.add_argument('email', type=str)
parser.add_argument('json', type=str)
parser.add_argument('type', type=str)


def setJSONFormat():
    args = parser.parse_args()
    json_type = args['json']
    if json_type == 'pretty':
        app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    else:
        app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

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

@app.route('/users/groups')
def users_with_groups():
    sql = text("select users.name, users.email, array_to_string(array_agg(distinct groups.name),',') as group_name, count(groups.id) from users JOIN user_group ON users.id = user_id JOIN groups on group_id = groups.id GROUP BY users.name, users.email ORDER BY 4 DESC;")
    result = db.engine.execute(sql)
    args = parser.parse_args()
    json_type = args['json']
    if json_type == 'pretty':
        return json.dumps([(dict(row.items())) for row in result], indent=4)
    else:
        return json.dumps([(dict(row.items())) for row in result], separators=(',', ':'))

@app.route('/users/group')
def users_with_group():
    sql = text("select users.id, users.name, users.email, count(group_id) as group_count from users JOIN user_group ON users.id = user_id GROUP BY 1,2,3 ORDER BY 4 ASC;")
    result = db.engine.execute(sql)
    args = parser.parse_args()
    json_type = args['json']
    if json_type == 'pretty':
        return json.dumps([(dict(row.items())) for row in result], indent=4)
    else:
        return json.dumps([(dict(row.items())) for row in result], separators=(',', ':'))

@app.route('/user/<int:user_id>/groups')
def groups_from_user(user_id):
    setJSONFormat()
    user = User.query.filter(User.id == user_id).first()
    return jsonify(user.groups)

@app.route('/group/users')
def group_with_users():
    sql = text("select groups.id, groups.name, count(user_id) as user_count from groups join user_group on groups.id = group_id GROUP BY 1,2 order by 3 DESC;")
    result = db.engine.execute(sql)
    args = parser.parse_args()
    json_type = args['json']
    if json_type == 'pretty':
        return json.dumps([(dict(row.items())) for row in result], indent=4)
    else:
        return json.dumps([(dict(row.items())) for row in result], separators=(',', ':'))

@app.route('/group/<int:group_id>/users')
def users_from_group(group_id):
    setJSONFormat()
    group = Group.query.filter(Group.id == group_id).first()
    print(group.users.all())
    return jsonify(group.users.all())

api.add_resource(GroupApi, '/group/<int:group_id>', endpoint = 'group')
api.add_resource(GroupsApi, '/groups', endpoint = 'groups')
api.add_resource(GroupModifyUserApi, '/groups/<int:group_id>/<string:command>_user/<int:user_id>')

api.add_resource(UserApi, '/user/<int:user_id>', endpoint = 'user')
api.add_resource(UsersApi, '/users', endpoint = 'users')

if __name__ == '__main__':
    app.run(debug=True)
