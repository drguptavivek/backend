# python package
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
        import backend.models_import

        # Seed initial data
        from backend.db_initializer.db_initializer import create_department
        create_department()
        from backend.db_initializer.db_initializer import create_faculty_cadre
        create_faculty_cadre()

        # Importing routes
        
    return app

