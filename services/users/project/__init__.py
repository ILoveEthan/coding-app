import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app(script_info=None):
	app = Flask(__name__)

	CORS(app)

	app.config.from_object(os.getenv('APP_SETTINGS'))
	db.init_app(app)

	from project.api.users import bp
	app.register_blueprint(bp)

	app.shell_context_processor({'app': app, 'db': db})
	return app