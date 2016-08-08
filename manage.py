import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from faker import Faker

from app import flask_app
from db import db
from random import randint
from models.user import User
from models.group import Group

migrate = Migrate(flask_app, db)
manager = Manager(flask_app)

manager.add_command('db', MigrateCommand)

@manager.command
def list_routes():
    import urllib
    output = []
    print(flask_app.url_map)

@manager.command
def seed_data_user():
    fake = Faker()
    fake_email = ["euismod.mauris@sapienimperdietornare.co.uk","montes.nascetur.ridiculus@Nunc.co.uk",
            "vitae.purus.gravida@orciin.com","Nunc.laoreet@In.co.uk","faucibus@congueelit.net",
            "ultrices.Duis.volutpat@risus.ca","Duis@dolor.edu","Cras.eu.tellus@Mauriseu.org","at@auctor.com",
            "ornare@Phasellusataugue.net","eu.metus.In@nonluctussit.co.uk","consequat.purus@rhoncusid.net",
            "nec@mollisdui.edu","vulputate.dui.nec@Aliquam.ca","magna.Nam.ligula@Donecfeugiatmetus.net",
            "pede@utaliquam.co.uk","sodales.elit@orcitincidunt.edu","elementum.dui.quis@nibhenimgravida.org",
            "Duis.ac.arcu@imperdietdictum.org","sed.orci.lobortis@mieleifend.edu","libero.Morbi@Aeneangravidanunc.org",
            "neque.pellentesque.massa@liberoat.co.uk","Mauris.eu@nisi.org","libero.Proin@ornare.edu",
            "massa.Integer@Aenean.ca","vestibulum.lorem.sit@arcu.org","ridiculus.mus@etnetus.edu",
            "et.libero.Proin@natoquepenatibuset.edu","id.libero@accumsaninterdum.co.uk",
            "volutpat.Nulla@inlobortistellus.co.uk","Aenean.egestas.hendrerit@urnaet.co.uk",
            "commodo.hendrerit.Donec@lectus.org","rhoncus@lorem.com","facilisis@rutrumlorem.co.uk",
            "dui.nec@iaculisaliquet.net","ridiculus.mus.Aenean@orciluctuset.edu","sed.pede.nec@lacusvariuset.edu",
            "a.sollicitudin@semperetlacinia.org","elit@Namtempor.ca","non.lorem.vitae@volutpatnuncsit.org",
            "mattis@diam.co.uk"]

    for _ in range(0,100):
        user = User(fake.name())
        user.email = fake_email[randint(0,40)]
        db.session.add(user)
        print("added %s" % user.name)
    db.session.commit()

@manager.command
def seed_data_group():
    fake = Faker()
    for x in range(0, 10):
        group = Group("Group_%s" % x)
        db.session.add(group)
        print("added %s" % group.name)
    db.session.commit()

@manager.command
def seed_data_user_group():
    for x in range(1,101):
        user = User.query.filter(User.id==x).first()
        group_id = randint(1,10)
        group = Group.query.filter(Group.id==group_id).first()
        group.users.append(user)
        db.session.commit()
        print("commited %s" % group.name)

if __name__ == '__main__':
    manager.run()
