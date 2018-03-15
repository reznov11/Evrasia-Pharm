# -*- coding: utf-8 -*-

import sys
import uuid
import psycopg2
from evrasia import create_app
from evrasia.models import db,User,Role
from flask_script import Manager
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate, MigrateCommand
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

app = create_app('evrasia.config.DevConfig')

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.shell
def make_shell_context():
	return dict(app=app, db=db)

@manager.command
def create_roles(roles={"admin":"Evrasia Website Administator","user":"Evrasia Website Normal User"}):
	try:
		for key, value in roles.iteritems():
			if key == 'admin':
				role_admin = Role(name=key, description=value)
				db.session.add(role_admin)
			elif key == 'user':
				role_user = Role(name=key, description=value)
				db.session.add(role_user)
		db.session.commit()
		return "Roles created"
	except (ValueError,IntegrityError) as identifier:
		db.session.rollback()
		return "Error %s", identifier

@manager.command
def initdbase():

	con = None

	try:
		con = psycopg2.connect("host='localhost' dbname='postgres' user='' password=''")
		con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
		cur = con.cursor()
		cur.execute("CREATE DATABASE evrasia")
		con.commit()
		print "Database created."

	except psycopg2.DatabaseError, e:
		if con:
			con.rollback()
		print 'Error %s' % e
		sys.exit(1)

	finally:
		if con:
			con.close()

@manager.command
def initadmin():
	admin_exist = User.query.filter_by(username='reznov', is_admin=True).first()
	if admin_exist:
		return "You can't create two admins"
	user = User()
	user.username = 'reznov'
	user.set_password('')
	user.email = ''
	user.address = ''
	user.telephone = ''
	admin_role = Role.query.filter_by(name="admin").first()
	if not admin_role:
		return "Administration roles not found, you need to create them"
	user.roles.append(admin_role)
	user.is_admin = True
	user.confirmed = True
	user.image = user.avatar(100)
	user.public_id = uuid.uuid5(uuid.NAMESPACE_DNS, user.telephone)
	db.session.add(user)
	db.session.commit()
	return 'User created.'

if __name__ == '__main__':
	manager.run()
	
