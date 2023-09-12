# python package
import click
from flask import Flask






def create_app():
    app = Flask(__name__, instance_relative_config=False)
    from config import ProdConfig, DevConfig
    app.config.from_object(ProdConfig)
    
    # Import the Initialized Flask extensions  
    # Import the db object and various models that have inherited the db object
    from .extensions import db, migrate, ma
    
    with app.app_context():
        # Set global values

        # Initialize globals
        db.init_app(app)
        migrate.init_app(app, db)
        ma.init_app(app)
        
        # Import Models
        # Used by Flask-Migrate
        import backend.models_import

        # Register the " flask --app backend init-db" command
        from backend.db_initializer.db_initializer import seed_db_command, empty_db_command
        app.cli.add_command(seed_db_command)
        app.cli.add_command(empty_db_command)

        # Importing routes
        
    return app

