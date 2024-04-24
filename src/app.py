#IMPORTACIONES
import os

from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Characters, Planets, Vehicles, CharactersFavorites, PlanetsFavorites, VehiclesFavorites

# Configuración de la aplicación Flask

app = Flask(__name__)
app.url_map.strict_slashes = False

#Configuracion de la base de datos

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Configuracion de la migracion

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Manejo de errores 
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Gererar sitemap
@app.route('/')
def sitemap():
    return generate_sitemap(app)



#----------------------------METODO USER----------------------------------------------------------------------------------------------------------------------------------------------

# METODO GET PARA OBTENER TODOS LOS USUARIOS------------------------ CON EXPLICACION

@app.route('/user', methods=['GET'])
def get_all_users():
    # Obtener todos los usuarios de la base de datos
    query_results = User.query.all()
    # Verifica si no hay resultados
    if not query_results:
        return jsonify({"msg" : "No hay usuarios en la base de datos"}), 404
    # Serializa los resultados
    results = [item.serialize() for item in query_results]
    # Crea la respuesta
    response_body = {
        "msg": "Hello, te muestro los usuarios que existen en la base de datos",
        "results": results
    }
    return jsonify(response_body), 200

# METODO GET PARA OBTENER TODOS LOS USUARIOS------------------------------------------------------- CON EXPLICACION

@app.route('/users/favorites', methods=['GET'])
def get_all_favorite():
    # Obtiene todos los usuarios
    users = User.query.all()

    # Verifica si no hay usuarios en la base de datos
    if not users:
        return jsonify({"msg": "No users found"}), 404

    # Lista para almacenar todos los favoritos
    all_favorites = []

    # Pasa sobre cada usuario para obtener sus favoritos
    for user in users:
        # Obtiene los favoritos de personajes del usuario actual
        characters_favorites = CharactersFavorites.query.filter_by(user_id=user.id).all()
        # Serializa los favoritos de personajes
        serialized_characters = [fav.serialize() for fav in characters_favorites]

       
        planets_favorites = PlanetsFavorites.query.filter_by(user_id=user.id).all()
        serialized_planets = [fav.serialize() for fav in planets_favorites]

        
        vehicles_favorites = VehiclesFavorites.query.filter_by(user_id=user.id).all()
        serialized_vehicles = [fav.serialize() for fav in vehicles_favorites]

        # Agrupa los favoritos del usuario
        user_favorites = {
            "user_id": user.id,
            "favorite_characters": serialized_characters,
            "favorite_planets": serialized_planets,
            "favorite_vehicles": serialized_vehicles
        }

        # Agrega los favoritos del usuario a la lista de todos los favoritos
        all_favorites.append(user_favorites)

    # Retorna la lista de todos los favoritos
    return jsonify({"msg": "Here are all the favorites", "results": all_favorites}), 200


#------------------------METODOS CHARACTERS--------------------------------------------------------------------------------------------------------------------------------------------


# METODO GET MOSTRAR TODOS LOS PERSONAJES 

@app.route('/people', methods=['GET'])
def get_all_people():

    query_results = Characters.query.all()
    results = list(map(lambda item: item.serialize(), query_results))
   
    if results == []:
        return jsonify({"msg" : "No hay personajes en la base de datos"}), 404

    response_body = {
        "msg": "Hello, te muestro todos los personajes",
        "results": results
    }

    return jsonify(response_body), 200


# METODO GET MOSTRAR PERSONAJES POR ID 

@app.route('/people/<int:people_id>', methods=['GET'])
def get_characters(people_id):

    characters = Characters.query.get(people_id)
   
    if characters == None:
        return jsonify({"msg" : "No existe el personaje"}), 404

    response_body = {
        "msg": "Te muestro un personaje",
        "results": characters.serialize()
    }

    return jsonify(response_body), 200


# METODO POST CREAR PERSONAJES -------------------------------------- CON EXPLICACION 

@app.route('/people', methods=['POST'])
def create_people():
    # Obtiene los datos del cuerpo de la solicitud en formato JSON
    body = request.json
    
    # Consulta si ya existe un personaje con el mismo nombre
    people_query = Characters.query.filter_by(name=body["name"]).first()
    
    # Verifica si no se encontró ningún personaje con el mismo nombre
    if people_query is None:
        # Crea un nuevo personaje con los datos del cuerpo de la solicitud
        new_characters = Characters(
            id=body["id"],
            name=body["name"],
            height=body["height"],
            mass=body["mass"],
            eye_color=body["eye color"],
            hair_color=body["hair color"],
            birth_year=body["birth_year"],
            skin_color=body["skin color"],
            gender=body["gender"]
        )
        # Agrega el nuevo personaje a la sesión de la base de datos
        db.session.add(new_characters)
        # Confirma la transacción, guardando el nuevo personaje en la base de datos
        db.session.commit()
        
        # Devuelve un mensaje indicando que el personaje se ha creado y un código de estado HTTP 200
        return jsonify("Personaje creado"), 200

    # Si ya existe un personaje con el mismo nombre, devuelve un mensaje indicando que el personaje ya existe y un código de estado HTTP 400
    return jsonify("El personaje ya existe"), 400


# METODO DELETE ELIMINAR PERSONAJES ----------------------- CON EXPLICACION

@app.route('/people/<int:people_id>', methods=['DELETE'])
def delete_person(people_id):
    # Busca el personaje en la base de datos por su ID
    characters = Characters.query.get(people_id)
    
    # Verifica si se encontró el personaje
    if characters:
        # Elimina el personaje de la sesión de la base de datos
        db.session.delete(characters)
        # Confirma la transacción, eliminando el personaje de la base de datos
        db.session.commit()
        
        # Devuelve un mensaje indicando que el personaje se ha eliminado correctamente y un código de estado HTTP 200
        return jsonify({"msg": "Personaje eliminado correctamente"}), 200
    else:
        # Si el personaje no se encuentra, devuelve un mensaje de error y un código de estado HTTP 404
        return jsonify({"error": "Personaje no encontrado"}), 404
    

# METODO POST AÑADIR FAVORITOS PERSONAJES----------------------CON EXPLICACION

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def create_favorite_characters(people_id):
    # Obtiene los datos 
    body = request.json
    
    # Verifica  usuario 
    check_user = User.query.filter_by(id=body["id"]).first()
    if check_user is None:
        # Si el usuario no existe, devuelve un mensaje de error y un código de estado HTTP 404
        return jsonify({"msg": "No existe el usuario"}), 404
    else:
        # Verifica  personaje 
        check_characters = Characters.query.filter_by(id=people_id).first()
        if check_characters is None:
            # Si el personaje no existe.......
            return jsonify({"msg": "No existe el personaje"}), 404
        else:
            # si el personaje ya está en favoritos..........
            check_favorite_characters = CharactersFavorites.query.filter_by(characters_id=people_id, user_id=body["id"]).first()
            if check_favorite_characters is None:
                # Si el personaje no está en favoritos, lo añade a la lista de favoritos del usuario
                new_favorite_characters = CharactersFavorites(user_id=body["id"], characters_id=people_id)
                db.session.add(new_favorite_characters)
                db.session.commit()
                # Devuelve un mensaje indicando que el personaje se añadió a favoritos y un código de estado
                return jsonify({"msg": "Personaje añadido a favoritos"}), 200
            else:
                # Si el personaje ya está en favoritos, devuelve un mensaje indicando que el personaje está repetido y un código de estado
                return jsonify({"msg": "Personaje repetido"}), 400


# METODO DELETE FAVORITOS PERSONAJES

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_characters(people_id):
    body = request.json
    check_user = User.query.filter_by(id=body["id"]).first()
    if check_user is None:
        return jsonify({"msg" : "El usuario no existe"}), 404
    else:
        check_characters = Characters.query.filter_by(id=people_id).first()
        if check_characters is None:
            return jsonify({"msg" : "El personaje no existe"}), 404
        else:
            favorite_characters = CharactersFavorites.query.filter_by(characters_id=people_id, user_id=body["id"]).first()
            if favorite_characters:
                #---------------SOLO CAMBIA .DELETE PARA ELIMINAR DE FAVORITOS------
                db.session.delete(favorite_characters)
                db.session.commit()
                return jsonify({"msg" : "¡Personaje eliminado de favoritos!"}), 200
            else:
                return jsonify({"msg" : "¡Personaje no encontrado en favoritos!"}), 404          

# METODO PUT ACTUALIZAR PERSONAJES

@app.route('/people/<int:people_id>', methods=['PUT'])
def update_characters(people_id):
    # Obtener los datos del cuerpo de la solicitud en formato JSON
    body = request.json
    
    # Buscar el personaje en la base de datos por su ID
    characters = Characters.query.get(people_id)
    
    # Verificar si se encontró el personaje
    if characters:
        # Actualizar los campos del personaje con los nuevos datos proporcionados
        characters.name = body.get("name", characters.name)
        characters.height = body.get("height", characters.height)
        characters.mass = body.get("mass", characters.mass)
        characters.eye_color = body.get("eye color", characters.eye_color)
        characters.hair_color = body.get("hair color", characters.hair_color)
        characters.birth_year = body.get("birth_year", characters.birth_year)
        characters.skin_color = body.get("skin color", characters.skin_color)
        characters.gender = body.get("gender", characters.gender)
        
        # Guardar los cambios en la base de datos
        db.session.commit()
        
        # Devolver un mensaje indicando que el personaje se ha actualizado correctamente y un código de estado HTTP 200
        return jsonify({"msg": "Personaje actualizado correctamente"}), 200
    else:
        # Si el personaje no se encuentra, devolver un mensaje de error y un código de estado HTTP 404
        return jsonify({"error": "Personaje no encontrado"}), 404 


#------------------------METODOS PLANETS-------------------------------------------------------------------------------------------------------------------------------------------------


# METODO GET MOSTRAR TODOS LOS PLANETAS 
@app.route('/planets', methods=['GET'])
def get_all_planets():

    query_results = Planets.query.all()
    results = list(map(lambda item: item.serialize(), query_results))
   
    if results == []:
        return jsonify({"msg" : "No hay planetas en la base de datos"}), 404

    response_body = {
        "msg": "Hello, te muestro todos planetas",
        "results": results
    }

    return jsonify(response_body), 200


# METODO GET id MOSTRAR PLANETAS 
@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_planet(planets_id):

    planet = Planets.query.get(planets_id)
   
    if planet == None:
        return jsonify({"msg" : "No existe planeta"}), 404

    response_body = {
        "msg": "Te muestro un planeta",
        "results": planet.serialize()
    }   

    return jsonify(response_body), 200


# METODO POST CREAR PLANETAS 
@app.route('/planets', methods=['POST'])
def create_planet():
    body = request.json
    
    planet_query = Planets.query.filter_by(name=body["name"]).first()
    
    if planet_query is None:
        new_planet = Planets(
            id=body["id"],
            name=body["name"],
            diameter=body["diameter"],
            rotation_speed=body["rotation_speed"],
            orbital_period=body["orbital_period"],
            gravity=body["gravity"],
            population=body["population"],
            climate=body["climate"],
            terrain=body["terrain"],
            surface_water=body["surface_water"]
        )
        db.session.add(new_planet)
        db.session.commit()

        return jsonify("Planeta creado"), 200

    return jsonify("El planeta ya existe"), 400


# METODO DELETE ELIMINAR PLANETAS 
@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):

    planet = Planets.query.get(planet_id)
    
    if planet:
        db.session.delete(planet)
        db.session.commit()
        
        return jsonify({"msg": "Planeta eliminado correctamente"}), 200
    else:

        return jsonify({"error": "Planeta no encontrado"}), 404


# METODO POST FAVORITOS PLANETAS   
@app.route('/favorite/planets/<int:planet_id>', methods=['POST'])
def create_favorite_planet(planet_id):
    body = request.json

    check_user = User.query.filter_by(id=body["id"]).first()
    
    if check_user is None:
        return jsonify({"msg" : "El usuario no existe"}), 404
    
    
    check_planet = Planets.query.filter_by(id=planet_id).first()
    
    if check_planet is None:
         return jsonify({"msg" : "El planeta no existe"}), 404
    
    
    check_favorite_planet = PlanetsFavorites.query.filter_by(planet_id=planet_id, user_id=body["id"]).first()
    
    if check_favorite_planet is None:
        
        new_favorite_planet = PlanetsFavorites(user_id=body["id"], planet_id=planet_id)
        db.session.add(new_favorite_planet)
        db.session.commit()
        
        return jsonify({"msg" : "Planeta añadido a favoritos"}), 200
    else:
        return jsonify({"msg" : "El planeta ya está en la lista de favoritos"}), 400   


# METODO DELETE FAVORITOS PLANETAS
@app.route('/favorite/planets/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    
    body = request.json
    
    check_user = User.query.filter_by(id=body["id"]).first()
    
    if check_user is None:
        return jsonify({"msg" : "El usuario no existe"}), 404
    
    else:
        check_planet = Planets.query.filter_by(id=planet_id).first()
        
        if check_planet is None:
            return jsonify({"msg" : "El planeta no existe"}), 404
        
        else:
            favorite_planet = PlanetsFavorites.query.filter_by(planet_id=planet_id, user_id=body["id"]).first()
            
            if favorite_planet:
                db.session.delete(favorite_planet)
                db.session.commit()
                return jsonify({"msg" : "¡Planeta eliminado de favoritos!"}), 200
            else:
                return jsonify({"msg" : "¡Planeta no encontrado en favoritos!"}), 404  

# METODO PUT ACTUALIZAR PLANETAS

@app.route('/planets/<int:planet_id>', methods=['PUT'])
def update_planet(planet_id):
    
    body = request.json
    
    planet = Planets.query.get(planet_id)
    
    if planet:
        planet.name = body.get("name", planet.name)
        planet.diameter = body.get("diameter", planet.diameter)
        planet.orbital_period = body.get("orbital_period", planet.orbital_period)
        planet.gravity = body.get("gravity", planet.gravity)
        planet.population = body.get("population", planet.population)
        planet.climate = body.get("climate", planet.climate)
        planet.terrain = body.get("terrain", planet.terrain)
        planet.surface_water = body.get("surface_water", planet.surface_water)
        db.session.commit()
        
        return jsonify({"msg": "Planeta actualizado correctamente"}), 200
    else:
        return jsonify({"error": "Planeta no encontrado"}), 404
   
    


#------------------------METODOS VEHICLES----------------------------------------------------------------------------------------------------------------------------------------------


#MOSTRAR TODOS LOS VEHICULOS METODO GET
@app.route('/vehicles', methods=['GET'])
def get_all_vehicles():

    query_results = Vehicles.query.all()
    results = list(map(lambda item: item.serialize(), query_results))
   
    if results == []:
        return jsonify({"msg" : "No hay vehiculos en la base de datos"}), 404

    response_body = {
        "msg": "Hello, te muestro todos los vehiculos",
        "results": results
    }

    return jsonify(response_body), 200

    
#MOSTRAR VEHICULOS POR ID METODO GET
@app.route('/vehicles/<int:vehicles_id>', methods=['GET'])
def get_vehicles(vehicles_id):

    vehicle = Vehicles.query.get(vehicles_id)
   
    if vehicle == None:
        return jsonify({"msg" : "No existe vehiculo"}), 404

    response_body = {
        "msg": "Te muestro un vehiculo ",
        "results": vehicle.serialize()
    }   

    return jsonify(response_body), 200


#METODO POST VEHICULOS
@app.route('/vehicles', methods=['POST'])
def create_vehicle():
    body = request.json
    
    vehicle_query = Vehicles.query.filter_by(model=body["model"]).first()
    
    if vehicle_query is None:
        new_vehicle = Vehicles(
            id=body["id"],
            model=body["model"],
            vehicle_class=body["vehicle_class"],
            manufacturer=body["manufacturer"],
            cost_in_credits=body["cost_in_credits"],
            lenght=body["lenght"],
            crew=body["crew"],
            passengers=body["passengers"],
            max_speed=body["max_speed"],
            cargo_capacity=body["cargo_capacity"],
            consumables=body["consumables"]
        )
        db.session.add(new_vehicle)
        db.session.commit()

        return jsonify("Vehículo creado"), 200

    return jsonify("El vehículo ya existe"), 400


#METODO DELETE ELIMINAR VEHICULOS 
@app.route('/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    
    vehicle = Vehicles.query.get(vehicle_id)
    
    if vehicle:
        db.session.delete(vehicle)
        db.session.commit()
        
        return jsonify({"msg": "Vehículo eliminado correctamente"}), 200
    else:
        return jsonify({"error": "Vehículo no encontrado"}), 404


# METODO POST FAVORITOS VEHICULOS            
@app.route('/favorite/vehicles/<int:vehicle_id>', methods=['POST'])
def create_favorite_vehicle(vehicle_id):
    
    body = request.json
    
    check_user = User.query.filter_by(id=body["id"]).first()
    
    if check_user is None:
        return jsonify({"msg" : "El usuario no existe"}), 404
    else:
        
        check_vehicle = Vehicles.query.filter_by(id=vehicle_id).first()
        
        if check_vehicle is None:
            return jsonify({"msg" : "El vehículo no existe"}), 404
        else:
            
            check_favorite_vehicle = VehiclesFavorites.query.filter_by(vehicle_id=vehicle_id, user_id=body["id"]).first()
            
            if check_favorite_vehicle is None:
                new_favorite_vehicle = VehiclesFavorites(user_id=body["id"], vehicle_id=vehicle_id)
                db.session.add(new_favorite_vehicle)
                db.session.commit()
                
                return jsonify({"msg" : "¡Vehículo añadido a favoritos!"}), 200
            else:
                return jsonify({"msg" : "¡Vehículo repetido en favoritos!"}), 400


# METODO DELETE FAVORITOS VEHICULOS
@app.route('/favorite/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete_favorite_vehicle(vehicle_id):
    
    body = request.json
    
    check_user = User.query.filter_by(id=body["id"]).first()
    
    if check_user is None:
        return jsonify({"msg" : "El usuario no existe"}), 404
    else:
        
        check_vehicle = Vehicles.query.filter_by(id=vehicle_id).first()
        
        if check_vehicle is None:
            return jsonify({"msg" : "El vehículo no existe"}), 404
        else:
            
            favorite_vehicle = VehiclesFavorites.query.filter_by(vehicle_id=vehicle_id, user_id=body["id"]).first()
            
            if favorite_vehicle:
                db.session.delete(favorite_vehicle)
                db.session.commit()
                
                return jsonify({"msg" : "¡Vehículo eliminado de favoritos!"}), 200
            else:
                return jsonify({"msg" : "¡Vehículo no encontrado en favoritos!"}), 404  




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)