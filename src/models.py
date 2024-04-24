from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
db = SQLAlchemy()



#----------MODELOS DE USER, CHARACTERS, PLANETS, VEHICLES---------------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    characters_favorites = db.relationship('CharactersFavorites', backref='user', lazy=True)
    planets_favorites = relationship('PlanetsFavorites', backref='user', lazy=True)
    vehicles_favorites = relationship('VehiclesFavorites', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email
            
            # do not serialize the password, its a security breach
        }
    
class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    mass = db.Column(db.Integer, unique=False, nullable=False)
    eye_color = db.Column(db.String(80), unique=False, nullable=False)
    hair_color = db.Column(db.String(80), unique=False, nullable=False)
    birth_year = db.Column(db.String(80), unique=False, nullable=False)
    skin_color = db.Column(db.String(80), unique=False, nullable=False)
    gender = db.Column(db.String(80), unique=False, nullable=False)
    characters_favorites = db.relationship('CharactersFavorites', backref='characters', lazy=True)

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "eye color": self.eye_color,
            "hair color": self.hair_color,
            "birth_year": self.birth_year,
            "skin color": self.skin_color,
            "gender": self.gender
            # do not serialize the password, its a security breach
        }
class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    diameter = db.Column(db.Integer, nullable=False)
    rotation_speed = db.Column(db.Integer, unique=False, nullable=False)
    orbital_period = db.Column(db.String(80), unique=False, nullable=False)
    gravity = db.Column(db.String(80), unique=False, nullable=False)
    population = db.Column(db.String(80), unique=False, nullable=False)
    climate = db.Column(db.String(80), unique=False, nullable=False)
    terrain = db.Column(db.String(80), unique=False, nullable=False)
    surface_water = db.Column(db.String(80), unique=False, nullable=False)
    planets_favorites = db.relationship('PlanetsFavorites', backref='planets', lazy=True)

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_speed": self.rotation_speed,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water
            # do not serialize the password, its a security breach
        }
    
class Vehicles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(120), nullable=False)
    vehicle_class = db.Column(db.String, nullable=False)
    manufacturer = db.Column(db.String, unique=False, nullable=False)
    cost_in_credits = db.Column(db.String(80), unique=False, nullable=False)
    lenght = db.Column(db.String(80), unique=False, nullable=False)
    crew = db.Column(db.String(80), unique=False, nullable=False)
    passengers = db.Column(db.String(80), unique=False, nullable=False)
    max_speed = db.Column(db.String(80), unique=False, nullable=False)
    cargo_capacity = db.Column(db.String(80), unique=False, nullable=False)
    consumables = db.Column(db.String(80), unique=False, nullable=False)
    vehicles_favorites = db.relationship('VehiclesFavorites', backref='vehicles', lazy=True)

    def __repr__(self):
        return '<Vehicles %r>' % self.model

    def serialize(self):
        return {
          "id": self.id,
         "model": self.model,
            "vehicle_class": self.vehicle_class,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "lenght": self.lenght,
            "crew": self.crew,
            "passengers": self.passengers,
            "max_speed": self.max_speed,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables
        }

 #----------MODELOS DE FAVORITOS---------------------------------   
    

class CharactersFavorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))

    def __repr__(self):
        return '<CharactersFavorites %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            # do not serialize the password, it's a security breach
        }
        
class PlanetsFavorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))

    def __repr__(self):
        return '<PlanetsFavorites %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            # do not serialize the password, it's a security breach
        }
        
class VehiclesFavorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'))

    def __repr__(self):
        return '<VehiclesFavorites %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            # do not serialize the password, it's a security breach
        }
