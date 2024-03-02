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
from models import db, Personaje, Planeta, Usuario, PlanetaFavorito, PersonajeFavorito
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
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

#GET METHOD
@app.route('/users', methods=['GET'])
def handle_users():
    usuario_query = Usuario.query.all()
    all_usuarios = list(map(lambda x: x.serialize(), usuario_query))

    return jsonify(all_usuarios), 200

@app.route('/people', methods=['GET'])
def hadle_personaje():
    personaje_query = Personaje.query.all()
    all_personajes = list(map(lambda x: x.serialize(), personaje_query))

    return jsonify(all_personajes), 200

@app.route('/planets', methods=['GET'])
def hadle_planeta():
    planeta_query = Planeta.query.all()
    all_planetas = list(map(lambda x: x.serialize(), planeta_query))

    return jsonify(all_planetas), 200

@app.route('/user/<int:id>', methods=['GET'])
def hadle_unico_usuario(id):
    usuario = Usuario.query.get(id)
    if usuario is None:
        raise APIException("Planet not found", status_code=404)
    return jsonify(usuario.serialize()), 200

@app.route('/planets/<int:id>', methods=['GET'])
def hadle_unico_planeta(id):
    planeta = Planeta.query.get(id)
    if planeta is None:
        raise APIException("User not found", status_code=404)
    return jsonify(planeta.serialize()), 200

@app.route('/people/<int:id>', methods=['GET'])
def hadle_unico_personaje(id):
    personaje = Personaje.query.get(id)
    if personaje is None:
        raise APIException("Character not found", status_code=404)
    return jsonify(personaje.serialize()), 200

@app.route('/users/favorites', methods=['GET'])
def listar_favoritos_usuario_actual():

    usuario_actual =  Usuario.query.all()  # Reemplaza esto con tu lógica real

    all_usuarios = list(map(lambda x: x.serialize(), usuario_actual))

    return jsonify(all_usuarios), 200

#POST METHOD
@app.route('/user', methods=['POST'])
def create_usuario():
    
    body = request.get_json()
    print(body)
    user1 = Usuario(email=body['email'], password=body['password'], nombre=body['nombre'], apellido=body['apellido'], fecha_subscripcion=body['fecha_subscripcion'])
    db.session.add(user1)
    db.session.commit()

    return jsonify({"msg": "The user has been created"}), 200

@app.route('/people', methods=['POST'])
def create_personaje():
    
    body = request.get_json()
    print(body)
    personaje1 = Personaje(nombre=body['nombre'], descripcion=body['descripcion'], altura=body['altura'], genero=body['genero'],)
    db.session.add(personaje1)
    db.session.commit()

    return jsonify({"msg": "The character has been created"}), 200

@app.route('/planet', methods=['POST'])
def create_planeta():
    
    body = request.get_json()
    print(body)
    personaje1 = Planeta(nombre=body['nombre'], poblacion=body['poblacion'], terreno=body['terreno'])
    db.session.add(personaje1)
    db.session.commit()

    return jsonify({"msg": "The planet has been created"}), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def agregar_planeta_favorito(planet_id):

    usuario_actual = Usuario.query.first()

    if usuario_actual:
        planeta = Planeta.query.get(planet_id)
        if planeta:
            favorito = PlanetaFavorito(usuario_id=usuario_actual.id, planeta_id=planet_id)
            db.session.add(favorito)
            db.session.commit()
            return jsonify({"msg": f"Planeta {planet_id} agregado a favoritos"}), 200
        else:
            raise APIException("Planeta no encontrado", status_code=404)
    else:
        raise APIException("Usuario no encontrado", status_code=404)

@app.route('/favorite/character/<int:character_id>', methods=['POST'])
def agregar_personaje_favorito(character_id):

    usuario_actual = Usuario.query.first()

    if usuario_actual:
        personaje = Personaje.query.get(character_id)
        if personaje:
            favorito = PersonajeFavorito(usuario_id=usuario_actual.id, personaje_id=character_id)
            db.session.add(favorito)
            db.session.commit()
            return jsonify({"msg": f"Personaje {character_id} agregado a favoritos"}), 200
        else:
            raise APIException("Personaje no encontrado", status_code=404)
    else:
        raise APIException("Usuario no encontrado", status_code=404)
    
#DELETE METHOD

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def eliminar_planeta_favorito(planet_id):

    usuario_actual = Usuario.query.first()

    if usuario_actual:
        favorito = PlanetaFavorito.query.filter_by(usuario_id=usuario_actual.id, planeta_id=planet_id).first()
        if favorito:
            db.session.delete(favorito)
            db.session.commit()
            return jsonify({"msg": f"Planeta {planet_id} eliminado de favoritos"}), 200
        else:
            raise APIException("Planeta no encontrado en favoritos", status_code=404)
    else:
        raise APIException("Usuario no encontrado", status_code=404)

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def eliminar_personaje_favorito(people_id):

    usuario_actual = Usuario.query.first()

    if usuario_actual:
        favorito = PersonajeFavorito.query.filter_by(usuario_id=usuario_actual.id, personaje_id=people_id).first()
        if favorito:
            db.session.delete(favorito)
            db.session.commit()
            return jsonify({"msg": f"Personaje {people_id} eliminado de favoritos"}), 200
        else:
            raise APIException("Personaje no encontrado en favoritos", status_code=404)
    else:
        raise APIException("Usuario no encontrado", status_code=404)

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
