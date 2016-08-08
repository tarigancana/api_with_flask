from db import db
from sqlalchemy.dialects.postgresql import JSON
import datetime
from sqlalchemy.sql.expression import text

class Group(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    created_at = db.Column(db.DateTime, server_default=text("(CURRENT_TIMESTAMP AT TIME ZONE 'UTC')"))
    updated_at = db.Column(db.DateTime())

    def __init__(self, name):
        self.name = name
        self.updated_at = datetime.datetime.utcnow()

    def clear_group(self):
        self.users = []
