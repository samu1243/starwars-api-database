from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=False, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorite_planet = db.relationship('FavoritePlanet', lazy=True)
    favorite_people = db.relationship('FavoritePeople', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            # do not serialize the password, its a security breach
        }
class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    height = db.Column(db.String(150), unique=False, nullable=False)
    mass = db.Column(db.String(150), unique=False, nullable=False)
    hair_color = db.Column(db.String(80), unique=False, nullable=False)
    skin_color = db.Column(db.String(80), unique=False, nullable=False)
    birth_year = db.Column(db.String(80), unique=False, nullable=False)
    eye_color = db.Column(db.String(40), unique=False, nullable=False)
    gender = db.Column(db.String(50), unique=False, nullable=False)
    created = db.Column(db.String(150), unique=False, nullable=False)
    edited = db.Column(db.String(150), unique=False, nullable=False)
    homeworld = db.Column(db.String(150), unique=False, nullable=False)
    url = db.Column(db.String(150), unique=False, nullable=False)
    description = db.Column(db.String(150), unique=False, nullable=True)
    uid = db.Column(db.String(150), unique=False, nullable=True)
    _id = db.Column(db.String(150), unique=False, nullable=True)
    favorite_people = db.relationship('FavoritePeople', lazy=True)
    
    def __init__(self, name, height, mass, hair_color, skin_color, birth_year, eye_color, gender, created, edited, homeworld, url, description=None, uid=None, _id=None):
        self.name = name
        self.height = height
        self.mass = mass
        self.hair_color = hair_color
        self.skin_color = skin_color
        self.birth_year = birth_year
        self.eye_color = eye_color
        self.gender = gender
        self.created = created
        self.edited = edited
        self.homeworld = homeworld
        self.url = url
        self.description = description
        self.uid = uid
        self._id = _id



class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    diameter = db.Column(db.Integer, unique=False, nullable=False)
    climate = db.Column(db.String(40), unique=False, nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)
    gravity = db.Column(db.String(80), unique=False, nullable=False)
    population = db.Column(db.String(100), unique=False, nullable=False)
    rotation_period = db.Column(db.String(80), unique=False, nullable=False)
    orbital_period = db.Column(db.String(80), unique=False, nullable=False)
    terrain = db.Column(db.String(150), unique=False, nullable=False)
    surface_water = db.Column(db.String(80), unique=False, nullable=False)
    url = db.Column(db.String(80), unique=True, nullable=False)
    created = db.Column(db.String(80), unique=False, nullable=False)
    edited = db.Column(db.String(80), unique=False, nullable=False)
    description = db.Column(db.String(80), unique=False, nullable=True)
    _id = db.Column(db.String(80), unique=False, nullable=True)
    uid = db.Column(db.String(80), unique=False, nullable=True)
    favorite_planet = db.relationship('FavoritePlanet', lazy=True)
    
    
    def __init__(self, id, diameter, climate, name, gravity, population, terrain, rotation_period, surface_water, url, created, edited, description=None, _id=None, uid=None):
        self.id = id
        self.diameter = diameter
        self.climate = climate
        self.name = name
        self.gravity = gravity
        self.population = population
        self.terrain = terrain
        self.rotation_period = rotation_period
        self.orbital_period = orbital_period
        self.surface_water = surface_water
        self.url = url
        self.created = created
        self.edited = edited
        self.description = description
        self._id = _id
        self.uid = uid




class FavoritePlanet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"))

    def __init__(self, user_id, planet_id):
        self.user_id = user_id
        self.planet_id = planet_id  


    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,    
        }

class FavoritePeople(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    people_id = db.Column(db.Integer, db.ForeignKey("people.id"))

    def __init__(self, user_id, people_id):
        self.user_id = user_id
        self.people_id = people_id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,             
            "people_id": self.people_id,
            }
