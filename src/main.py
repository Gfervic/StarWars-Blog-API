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
from models import db, User, Character, Planet, FavChar, FavPlan
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# people = [
#     { "name": "Obi-Wan Kenobi", "age": 54 },
#     { "name": "Jar Jar Binks", "age": 34 },
#     { "name": "Luke Skywalker", "age": 45 }
# ]

# planets = [
#     {"name": "Tatooine", "population": "200000", "terrain": "desert"},
#     {"name": "Yavin IV", "population": "1000", "terrain": "jungle"}
# ]

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# [GET] /people Get a list of all the people in the database
@app.route('/people', methods=['GET'])
def list_people():
    body = request.get_json()
    json_text = jsonify(body)
    return json_text

# [GET] /people/<int:people_id> Get a one single people information
@app.route('/people/<int:character_id>', methods=['GET'])
def get_character(character_id):
    print("This is the position to show: ",character_id)
    body = request.get_json()
    character1 = Character.query.get(character_id)
    print(character1)
    return jsonify(character1.serialize()), 200

# [GET] /planets Get a list of all the planets in the database
@app.route('/planets', methods=['GET'])
def list_planets():
    body = request.get_json()
    json_text = jsonify(body)
    return json_text

# [GET] /planets/<int:planet_id> Get one single planet information
@app.route('/planets/<int:planet_id>', methods=['GET'])
def list_planet(planet_id):
    print("This is the position to show: ",planet_id)
    body = request.get_json()
    planet1 = Planet.query.get(planet_id)
    print(planet1)
    return jsonify(planet1.serialize()), 200

# [GET] /users Get a list of all the blog post users
@app.route('/users', methods=['GET'])
def list_user():
    users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), users))

    return jsonify(all_users), 200

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
