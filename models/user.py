from app import db
from sqlalchemy.dialects.postgresql import JSON
import datetime
from sqlalchemy.sql.expression import text
from sqlalchemy import UniqueConstraint

groups = db.Table('user_group',
        db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
        db.Column('group_id', db.Integer, db.ForeignKey('groups.id')),
        db.Column('created_at',db.DateTime, server_default=text("(CURRENT_TIMESTAMP AT TIME ZONE 'UTC')")),
        UniqueConstraint('user_id', 'group_id', name='user_id_group_id_unique_key')
)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String())
    groups = db.relationship('Group', secondary=groups, backref=db.backref('users', lazy='dynamic'), cascade="delete")
    created_at = db.Column(db.DateTime, server_default=text("(CURRENT_TIMESTAMP AT TIME ZONE 'UTC')"))
    updated_at = db.Column(db.DateTime())

    def __init__(self, name):
        self.name = name
        self.updated_at = datetime.datetime.utcnow()
