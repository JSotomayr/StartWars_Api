import os
from flask_admin import Admin

from models import db, User, PeopleDetail, People, Species, SpeciesDetails, Starship, StarshipDetail
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    

    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Starship, db.session))
    admin.add_view(ModelView(StarshipDetail, db.session))
    admin.add_view(ModelView(Species, db.session))
    admin.add_view(ModelView(SpeciesDetails, db.session))
    admin.add_view(ModelView(People, db.session))
    admin.add_view(ModelView(PeopleDetail, db.session))


