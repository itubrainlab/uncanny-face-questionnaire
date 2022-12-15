from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path, mkdir
from pathlib import Path
import sys

db = SQLAlchemy()
DB_NAME = 'database.db'
CATALOGUE_NAME = 'image_catalogue.json'

def make_image_catalogue():
    import json
    IMAGE_FOLDER = Path("website/static/images/")

    imageid = 0
    catalogue = {}

    for cat in IMAGE_FOLDER.glob('*'):
        catname = cat.name
        catalogue[catname+'_first'] = imageid+1
        for img in cat.glob('*.png'):
            print(img)
            imageid += 1
            catalogue[imageid] = {
                'id' : imageid,
                'filepath' : str(img),
                'type' : catname
            }
        catalogue[catname+'_last'] = imageid
    catalogue['last'] = imageid
    # Make the json file
    json_object = json.dumps(catalogue, indent=4)
    with open("instance/"+CATALOGUE_NAME, "w") as outfile:
        outfile.write(json_object)

def create_app():
    if not path.exists("instance"):
        mkdir("instance")

    if not path.exists('instance/' + CATALOGUE_NAME):
        make_image_catalogue()
        print('Created image catalogue!', file=sys.stdout)
    # Init app
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config['SECRET_KEY'] = 'nL32Ex0ZpV1cIw7KFcjW'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    
    db.init_app(app)

    # Import URL paths
    from .views import views
    app.register_blueprint(views, urlprefix='/')
    

    # Import and init database models
    from .models import User, Rating, Submit
    if not path.exists('instance/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!', file=sys.stdout)

    return app

    