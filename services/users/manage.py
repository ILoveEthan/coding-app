import unittest
import coverage
from flask.cli import FlaskGroup
from project import create_app, db
from project.api.models import User

COV = coverage.coverage(
	branch=True,
	include='project/*',
	omit=[
		'project/tests/*',
		'project/config.py',
	]
)
COV.start()

app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command()
def recreate_db():
	db.drop_all()
	db.create_all()
	db.session.commit()

@cli.command()
def seed_db():
	db.session.add(User(username='test', email='test@gmail.com', password='123456'))
	db.session.commit()

@cli.command()
def test():
	tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
	result = unittest.TextTestRunner(verbosity=2).run(tests)
	if result.wasSuccessful():
		return 0
	return 1

@cli.command()
def cov():
	tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
	result = unittest.TextTestRunner(verbosity=2).run(tests)
	if result.wasSuccessful():
		COV.stop()
		COV.save()
		print('Coverage Summary:')
		COV.report()
		COV.html_report()
		COV.erase()
		return 0
	return 1

if __name__ == '__main__':
	cli()