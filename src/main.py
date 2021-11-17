"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
import datetime

from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required ,JWTManager

from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Species, SpeciesDetails, User

#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_KEY')  # Change this!
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


@app.route('/login', methods=['POST'])
def login():
    email, password = request.json.get('email', None), request.json.get('password', None)

    if email and password:
        user= User.get_by_email(email)

        if user:
            """check PASSWORD"""
            access_token = create_access_token(identity=user.id, datetime=timedelta(hours=12))
            return jsonify({'token': access_token}), 200

    return jsonify({'error':'Invalid Data'}), 400


@app.route('/user', methods=['GET'])
def get_user():
    users = User.get_all()

    return jsonify(users.to_dict()), 200


@app.route('/user/<int:id>/favourite', methods=['GET'])
@jwt_required
def get_fav(id):
    user = User.get_by_id(id)
    token_id = get_jwt_identity

    if token_id == id:
        pass
        """return favs"""

    return jsonify({'message':'User not found'}), 404    

@app.route('/species/', methods=['GET'])
def get_all_species():
    species = Species.get_all()

    if species:
        return jsonify(species.to_dict()), 200

    return jsonify({'message':'Species not found'}), 400


@app.route('/species/<int:id>', methods=['GET'])
def get_species(id):
    all_species = Species.get_by_id(id)

    if all_species:
        return jsonify(species.to_dict()), 200

    return jsonify({'message':'Species not found'}), 400



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
