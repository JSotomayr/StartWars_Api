"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from datetime import timedelta, datetime

from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS


from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from utils import APIException, generate_sitemap
from admin import setup_admin
from sqlalchemy import exc
from werkzeug.security import check_password_hash, generate_password_hash
from models import db, User, People, PeopleDetail, Species, SpeciesDetails, Starship, StarshipDetail

#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_KEY")
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
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if email and password:
        user = User.get_by_email(email)

        if user and check_password_hash(user._password, password) and user._is_active:
            """ password = User.get_by_password(password) """ #just in case for species we keep it
            access_token = create_access_token(identity=user.to_dict(), expires_delta=timedelta(days=30))
            return jsonify({'token': access_token}), 200
    
        return jsonify({'error': 'Invalid information'}), 400
    return jsonify({"msg": "wrong info"})


@app.route('/user', methods=['GET'])
def get_user():
    users = User.get_all()

    if users:
        users_list = [users.to_dict() for user in users]
        return jsonify(users_list), 200
    
    return jsonify({'error': 'Users not found'})


@app.route('/user', methods=['POST'])
def create_user():
    new_email = request.json.get('email', None)
    new_username = request.json.get('username', None)
    new_password = request.json.get('password', None)

    if not (new_email and new_username and new_password):
        return jsonify({'error': 'Missing user'}), 400

    user_created = User(email=new_email, username=new_username, _password=generate_password_hash(new_password, method='pbkdf2:sha256', salt_length=16))

    try:
        user_created.create()
    except exc.IntegrityError:
        return jsonify({'error': 'Fail in creating user'}), 400
    
    account = User.get_by_email(new_email)
    access_token = create_access_token(identity=account.to_dict(), expires_delta=timedelta(days=30))
    return jsonify({'token': access_token}), 200

                # GET USER BY ID

@app.route('/user/<int:id>', methods=['GET'])
def get_user_by_id(id):
    user = User.get_by_id(id)

    if user:
        return jsonify(user.to_dict()), 200

        return jsonify({'error': 'User is not found'}), 404

@app.route('/user/<int:id>/favourite', methods=['GET'])
@jwt_required
def get_fav(id):
    token_id = get_jwt_identity()

    if token_id == id:
        favourites = Favourite.get_all()
        return favourite

    return jsonify({'error': 'You are not authorized'})


    # GET STARSHIP
@app.route('/starship', methods=['GET'])
def get_starships():
    starships = Starship.get_all()

    if starships:
        starship_list = [starship.to_dict() for starship in starships]
        return jsonify(starship_list), 200

    return jsonify({'error': 'Starship not found'}), 404


            #GET BY (STARSHIPS ID)
@app.route('/starship/<int:id>', methods=['GET'])
def get_starship_by_id(id):
    starship = Starship.get_by_id(id)
    if starship:
        return jsonify(starship.to_dict()), 200

    return jsonify({'error':"Starship not found"}), 404


@app.route('/user/<int:id_user>/favourite-starship/<int:id_starship>', methods=['POST'])
@jwt_required()
def add_favstarship(id_user,id_starship):
    token_id = get_jwt_identity()

    if token_id.get("id") == id_user:
        user = User.get_by_id(id_user)
        starship = Starship.get_by_id(id_starship)

        if user and starship:
            add_fav = user.add_fav_starship(starship)
            fav_starships = [starship.to_dict() for starship in add_fav]
            return jsonify(fav_starships), 200

    return jsonify({'error': 'Starship favorite not found'}), 404


@app.route('/user/<int:id_user>/favourite-people/<int:id_people>', methods=['POST'])
@jwt_required()
def create_fav(id_user,id_people):
    token_id = get_jwt_identity()

    if token_id.get("id") == id_user:
        user = User.get_by_id(id_user)
        people = People.get_by_id(id_people)

        if user and people:
            add_people = user.new_fav_people(people)
            fav_people = [people.to_dict() for people in add_people]
            return jsonify(fav_people), 200

    return jsonify({'error': 'No favourites'}), 404


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
