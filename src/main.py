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
from models import db, User, Character, Planet, FavPlan, FavChar
#from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db, compare_type = True)
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
    # lista de instancias de clase
    all_people = Character.query.all() 
    all_people = list(map(lambda x: x.serialize(), all_people))
    return jsonify(all_people), 200

# [GET] /people/<int:people_id> Get a one single people information
@app.route('/people/<int:character_id>', methods=['GET'])
def get_character(character_id):
    # print("This is the position to show: ",character_id)
    character1 = Character.query.get(character_id)
    # print(character1)
    return jsonify(character1.serialize()), 200

# [GET] /planets Get a list of all the planets in the database
@app.route('/planets', methods=['GET'])
def list_planets():
    return jsonify(list(map(lambda x: x.serialize(), Planet.query.all()))), 200

# [GET] /planets/<int:planet_id> Get one single planet information
@app.route('/planets/<int:planet_id>', methods=['GET'])
def list_planet(planet_id):
    planet1 = Planet.query.get(planet_id)
    print(planet1)
    return jsonify(planet1.serialize()), 200

# [GET] /users Get a list of all the blog post users
@app.route('/users', methods=['GET'])
def list_user():
    return jsonify(list(map(lambda x: x.serialize(), User.query.all()))), 200

# [GET] /users/favorites Get all the favorites that belong to the current user.
@app.route('/<int:user_id>/favorites', methods=['GET'])
def user_favorites(user_id):
    fav_character = FavChar.query.filter_by(user_id=user_id)
    fav_character = list(map(lambda x: x.serialize(), fav_character))

    fav_planet = FavPlan.query.filter_by(user_id=user_id)
    fav_planet = list(map(lambda x: x.serialize(), fav_planet))

    all_favorites = fav_character + fav_planet
    
    return jsonify(all_favorites), 200

# [POST] /favorite/planet/<int:planet_id> Add a new favorite planet to the current user with the planet id = planet_id.
@app.route('/<int:user_id>/favorite/planet/<int:planet_id>', methods=['POST'])
def list_favorite_planet(user_id, planet_id):
    fav_planet = FavPlan(user_id=user_id, planet_id=planet_id)
    db.session.add(fav_planet)
    db.session.commit()

    return jsonify(fav_planet.serialize()), 200

# [POST] /favorite/people/<int:planet_id> Add a new favorite people to the current user with the people id = people_id.


# [DELETE] /favorite/planet/<int:planet_id> Delete favorite planet with the id = planet_id.

# [DELETE] /favorite/people/<int:people_id> Delete favorite people with the id = people_id.

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
