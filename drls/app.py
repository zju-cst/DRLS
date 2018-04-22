# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask, render_template

from drls import commands, public, user
from drls.extensions import bcrypt, cache, csrf_protect, db, debug_toolbar, login_manager, migrate, webpack
from drls.settings import ProdConfig
from drls.utils import JSONR
from filelock import Timeout, FileLock

import os


def create_app(config_object=ProdConfig):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    register_user_variable(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    webpack.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    return None


def register_errorhandlers(app):
    """Register error handlers."""
    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template('{0}.html'.format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Register shell context objects."""
    def shell_context():
        """Shell context objects."""
        return {
            'db': db,
            'User': user.models.User}

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.urls)

def register_user_variable(app):
    app.config.lock_file_path = os.path.join(app.config['UPLOAD_FOLDER'],app.config['LOCK_FILE_NAME'])
    app.config.seed_file_path = os.path.join(app.config['UPLOAD_FOLDER'],app.config['RANDOMSEED_FILE_NAME'])
    app.config.xls_file_path  = os.path.join(app.config['UPLOAD_FOLDER'], app.config['STUDATA_FILE_NAME'])
    app.config.num_file_path = os.path.join(app.config['UPLOAD_FOLDER'],app.config['RANDOMNUM_FILE_NAME'])

    app.config.lock_file_lock_path = os.path.join(app.config['UPLOAD_FOLDER'],app.config['LOCK_FILE_NAME']+'.lock')
    app.config.seed_file_lock_path = os.path.join(app.config['UPLOAD_FOLDER'],app.config['RANDOMSEED_FILE_NAME']+'.lock')
    app.config.xls_file_lock_path  = os.path.join(app.config['UPLOAD_FOLDER'], app.config['STUDATA_FILE_NAME']+'.lock')
    app.config.num_file_lock_path = os.path.join(app.config['UPLOAD_FOLDER'],app.config['RANDOMNUM_FILE_NAME']+'.lock')

    app.config.num_file_lock = FileLock(app.config.num_file_lock_path)
    app.config.seed_file_lock = FileLock(app.config.seed_file_lock_path)
    app.config.xls_file_lock = FileLock(app.config.xls_file_lock_path)
    app.config.lock_file_lock = FileLock(app.config.lock_file_lock_path)
