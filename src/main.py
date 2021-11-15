"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Species, SpeciesDetails
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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


""" @app.route('/user', methods=['GET'])
def get_user():
    users = User.get_all()

    return jsonify(response_body), 200


@app.route('/user/<int:id>', methods=['GET'])
def get_user_by_id(id):
    user = User.get_by_id(id)

    if user:
        return jsonify(user.to_dict()), 200

    return jsonify({'message':'User not found'}), 404     """

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
