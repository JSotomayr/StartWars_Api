"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os


from datetime import timedelta, datetime

from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
#                       libreria FLASK


from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

#                       libreria sqalchemy !!!
from sqlalchemy import exc

from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Planet, PlanetDetail, User



#                       FLASK
app = Flask(__name__)
app.url_map.strict_slashes = False

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#                       Configuración token
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_KEY")
jwt = JWTManager(app)


MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)



#                           POST login 

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if email and password:
        user = User.get_by_email(email)

        if user:
            access_token = create_access_token(identity=user.to_dict(), expires_delta=timedelta(days=30))
            return jsonify({'token': access_token}), 200
    
    return jsonify({'error': 'Invalid information'}), 400

#                           GET (user) 

@app.route('/user', methods=['GET'])
def get_user():
    users= User.get_all()
    all_users=[user.to_dict() for user in users]
    return jsonify(all_users), 200

#                           POST user 


@app.route('/user', methods=['POST'])
def create_user():
    new_user=request.json.get('username', None)
    new_email=request.json.get('email', None)
    new_password=request.json.get('password', None)
    
    if not (new_user and new_email and new_password):
        return jsonify({'error':'missing user'}), 400

    user_created= User(username=new_user, email=new_email, _password=new_password)

    try:
        user_created.create()
    except exc.IntegrityError:
        return jsonify({'error': 'fail in data'}), 400

    account = User.get_by_email(new_email)
    access_token = create_access_token(identity=account.to_dict(), expires_delta=timedelta(days=30))
    return jsonify({'token': access_token}), 200



#                       GET user ID (FOLKEN NO LO TIENE)
@app.route('/user/<int:id>', methods=['GET'])
def get_user_by_id(id):
    user = User.get_by_id_user(id)

    if user:
        return jsonify(user.to_dict()), 200

        return jsonify({'error': 'user not found'}), 404




#                           GET (id favorites) 
@app.route('/user/<int:id>/favourite', methods=['GET'])
@jwt_required
def get_fav(id):
    token_id = get_jwt_identity()

    if token_id == id:
        favourites = Favourite.get_all()
        return favourite

    return jsonify({'error': 'Not authorized'})


#                           GET planet 
@app.route('/planet', methods=['GET'])

def get_planets():
    planets = Planet.get_all_planets()

    if planets:
        planet_list = [planet.to_dict() for planet in planets]
        return jsonify(planet_list), 200

    return jsonify({'message': "Planet not found"}), 404


#                           GET FAVORITE PLANET
@app.route('/user/<int:id_user>/favourite-planet/<int:id_planet>', methods=['POST'])
@jwt_required()
def add_favplanet(id_user,id_planet):
    token_id = get_jwt_identity()

    if token_id.get("id") == id_user:
        user = User.get_by_id(id_user)
        planet = Planet.get_by_id(id_planet)


        if user and planet:
            add_fav = user.add_fav_planet(planet)
            fav_planets = [planet.to_dict() for planet in add_fav]
            return jsonify(fav_planets), 200

    return jsonify({'error': 'Planet fav not found'}), 404



#                           GET (id planet) 
@app.route('/planet/<int:id>', methods=['GET'])
def get_planet_by_id(id):

    planet = Planet.get_by_id(id)
    if planet:
        return jsonify(planet.to_dict()), 200
  

    return jsonify({'error': "PlanetId not found"}), 404




# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
