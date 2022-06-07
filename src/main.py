"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, make_response
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, People, FavoritePeople, FavoritePlanet
#from models import Person
import requests
import json


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

URL_BASE = 'https://www.swapi.tech/api/'

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def handle_user():
    users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), users))
    response_body = {'msg':'Hello, this is your /GET users response', 'results': all_users}
    return jsonify(response_body), 250
#----------------------------people--------------------------------------
@app.route('/people', methods=['GET'])
def handle_people():
    response = requests.get(f'{URL_BASE}/people')
    response_decoded = response.json()
    people = People.query.all()
    if len(people) == 0:
        for people in response_decoded["results"]:
            response_one_people = requests.get(people["url"])
            response_one_people_decoded = response_one_people.json()
            response_one_people_decoded["result"]
            one_people = People(**response_one_people_decoded["result"]["properties"], _id=response_one_people_decoded["result"]["_id"], uid=response_one_people_decoded["result"]["uid"])
            db.session.add(one_people)
        db.session.commit()
    return response_decoded, 200

@app.route('/people/<int:people_id>', methods = ['GET'])
def handle_individual(people_id):
    response = requests.get(f'{URL_BASE}/people/{people_id}')
    return response.json()

@app.route('/favorite/people/<int:people_id>', methods = ['POST', 'DELETE'])
def post_favorite_people(people_id):
    user = list(User.query.filter_by(is_active=True))
    people = list(People.query.filter_by(uid=people_id))
    if request.method == 'POST':
        if len(user) > 0 and len(people) > 0:
            my_favorite_people = FavoritePeople(user[0].id, people[0].id)
            db.session.add(my_favorite_people)
            db.session.commit()
        return {"msg": f"Favorite people created with user id {user[0].id} and people id {people[0].id}"}, 200
    else:
        favorite_people = FavoritePeople.query.filter_by(user_id=user[0].id, people_id=people[0].id)
        if favorite_people is None:
            raise APIException('Favorite not found', status_code=404)
        db.session.delete(favorite_people[0])
        db.session.delete
        return {"msg": f"Favorite eliminated with user id: {user[0].id} and people id: {people[0].id}"}


##---------------------------planets-----------------------------------


@app.route('/planets', methods=['GET'])
def handle_planets():
    response = requests.get(f'{URL_BASE}/planets')
    response_decoded = response.json()
    planets = Planet.query.all()
    if len(planets) == 0:
        for planet in response_decoded["results"]:
            response_one_planet = requests.get(planet['url'])
            response_one_planet_decoded = response_one_planet.json()
            response_one_planet_decoded['result']
            one_planet= Planet(**response_one_planet_decoded["result"]["properties"], description=response_one_planet_decoded["result"]["_id"], uid=response_one_planet_decoded["result"]["uid"])
            db.session.add(one_planet)
        db.session.commit()
    return response_decoded, 200

@app.route('/planets/<int:planets_id>', methods = ['GET'])
def handle_individual_planet(planets_id):
    response = requests.get(f'{URL_BASE}/planets/{planets_id}')
    return response.json()

@app.route("/favorite/planet/<int:planet_id>", methods = ['POST', 'DELETE'])
def post_favorite_planet(planet_id):
    user = list(User.query.filter_by(is_active=True))
    planet = list(Planet.query.filter_by(uid=planet_id))
    if request.method == 'POST':
        if len(user) > 0 and len(planet) > 0:
            my_favorite_planet = FavoritePlanet(user[0].id, planet[0].id)
            db.session.add(my_favorite_planet)
            db.session.commit()
        return {"msg": f"Favorite created with user id: {user[0].id} and planet id: {planet[0].id}"}, 200
    else: 
        favorite_planet = FavoritePlanet.query.filter_by(user_id= user[0].id, planet_id= planet[0].id)
        if favorite_planet is None:
            raise APIException('Favorite not found', status_code=404)
        db.session.delete(favorite_planet[0])
        db.session.commit
        return {"msg": f"Favorite eliminated with user id: {user[0].id} and planet id: {planet[0].id}"}, 200
    
@app.route('/users/favorites', methods = ['GET'])
def handle_user_favorites():
    favorites = []
    user = list(User.query.filter_by(is_active=True))
    for favorite_planet in user[0].favorite_planet:
        favorites.append(favorite_planet.serialize())
    response = {'msg':'Here are your favorite planets', 'results':favorites}
    for favorite_people in user[0].favorite_people:
        favorites.append(favorite_people.serialize())
    response = {'msg':'Here are your favorite people', 'results':favorites}        
    return jsonify(response),200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
