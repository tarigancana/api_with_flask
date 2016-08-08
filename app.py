from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse, abort
from flask_sqlalchemy import SQLAlchemy
from flask.json import JSONEncoder
from sqlalchemy import text
import json
import os

flask_app = Flask(__name__)
api = Api(flask_app)
flask_app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from models.user import User
from models.group import Group

class FlaskApiEncoder(JSONEncoder):
    item_separator = ','
    key_separator  = ':'
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

flask_app.json_encoder = FlaskApiEncoder

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
        flask_app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    else:
        flask_app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

from resources.user_api import UserApi, UsersApi
from resources.group_api import GroupApi, GroupsApi, GroupModifyUserApi

api.add_resource(UserApi, '/user/<int:user_id>')
api.add_resource(UsersApi, '/users')

api.add_resource(GroupApi, '/group/<int:group_id>', endpoint = 'group')
api.add_resource(GroupsApi, '/groups', endpoint = 'groups')
api.add_resource(GroupModifyUserApi, '/groups/<int:group_id>/<string:command>_user/<int:user_id>')

if __name__ == '__main__':
    flask_app.run(debug=True)
