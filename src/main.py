"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
<<<<<<< HEAD
from datetime import timedelta, datetime


=======

>>>>>>> d311cad890ea42b8b001c2524e32a3f41be4c9e3
from datetime import timedelta, datetime
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
<<<<<<< HEAD
from sqlalchemy import exc
=======
>>>>>>> d311cad890ea42b8b001c2524e32a3f41be4c9e3
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from utils import APIException, generate_sitemap
from admin import setup_admin
from sqlalchemy import exc
<<<<<<< HEAD
from models import db, User, Species, SpeciesDetails
=======
from models import db, User, Favourite, FavouritePeople, People, PeopleDetail, Species, SpeciesDetails
>>>>>>> d311cad890ea42b8b001c2524e32a3f41be4c9e3

#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_KEY')
jwt = JWTManager(app)


MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/to_dict errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/login', methods=['POST'])
def login():
    email, password = request.json.get('email', None), request.json.get('password', None)

    if email and password:
        user = User.get_by_email(email)

        if user:
            password = User.get_by_password(password)
            access_token = create_access_token(identity=user.to_dict(), expires_delta=timedelta(days=30))
            return jsonify({'token': access_token}), 200
    
        return jsonify({'error': 'Invalid information'}), 400
    return jsonify({"msg": "wrong info"})


@app.route('/user', methods=['GET'])
def get_user():
    users = User.get_all()

    return jsonify(users.to_dict()), 200


@app.route('/user', methods=['POST'])
def create_user():
    new_email = request.json.get('email', None)
    new_username = request.json.get('username', None)
    new_password = request.json.get('password', None)

    if not (new_email and new_username and new_password):
        return jsonify({'error': 'Missing user'}), 400

    user_created = User(email=new_email, username=new_username, _password=new_password) 

    try:
        user_created.create()
    except exc.IntegrityError:
        return jsonify({'error': 'Fail in creating user'}), 400
    
    account = User.get_by_email(new_email)
    access_token = create_access_token(identity=account.to_dict(), expires_delta=timedelta(days=30))
    return jsonify({'token': access_token}), 200


@app.route('/species/', methods=['GET'])
def get_all_species():
    specie_s = Species.get_all()

    if specie_s:
        all_species = [species.to_dict() for species in specie_s]
        return jsonify(all_species), 200

    return jsonify({'message':'Species not found'}), 400


@app.route('/species/<int:id>/speciesdetails', methods=['GET'])
def get_species(id):
    all_species = Species.get_by_id_speciesdetails(id)

    if all_species:
        return jsonify(all_species.to_dict()), 200

    return jsonify({'message':'Species not found'}), 400
@app.route('/people', methods=['GET'])
def get_all_people():
    characters = People.get_all()

    if characters:
        character_list = [character.serialize() for character in characters] 
        return jsonify({character_list}), 200


    return jsonify({'error': 'Characters not found'}), 400


@app.route('/people/<int:id>', methods=['GET'])
def get_character(id):
    character = People.get_by_id(id)

    if character:
        return jsonify(character.serialize()), 200

@app.route('/user/<int:id_user>/favourite-species/<int:id_species>', methods=['POST'])
@jwt_required()
def add_favspecies(id_user,id_species):
    token_id = get_jwt_identity()
    print(token_id)

    if token_id.get("id") == id_user:
        user = User.get_user_by_id(id_user)
        species = Species.get_by_id(id_species)
        
        if user and species:
            add_fav = user.add_fav_species(species)
            fav_species = [species.to_dict() for species in add_fav]
            return jsonify(fav_species),200

    return jsonify({'error': 'Not authorized'}),404

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)