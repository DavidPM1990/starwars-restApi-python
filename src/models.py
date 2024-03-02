from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()
  
class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    nombre = db.Column(db.String(250))
    apellido = db.Column(db.String(250))
    fecha_subscripcion = db.Column(db.DateTime)
    planetas_favoritos = relationship('PlanetaFavorito', back_populates='usuario', cascade='all,delete')
    personajes_favoritos = relationship('PersonajeFavorito', back_populates='usuario', cascade='all,delete')
    
    def __repr__(self):
        return '<Usuario %r>' % self.nombre

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "fecha_subscripcion": self.fecha_subscripcion,
            "planetas_favoritos": [favorito.planeta.serialize() for favorito in self.planetas_favoritos],
            "personajes_favoritos": [favorito.personaje.serialize() for favorito in self.personajes_favoritos]
            # do not serialize the password, its a security breach
        }

class Planeta(db.Model):
    __tablename__ = 'planeta'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False)
    poblacion = db.Column(db.Integer)
    terreno = db.Column(db.Integer)
    planetas_favoritos = relationship('PlanetaFavorito', back_populates='planeta', cascade='all,delete')


    def __repr__(self):
        return '<Planeta %r>' % self.nombre

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "poblacion": self.poblacion,
            "terreno": self.terreno

        }

class Personaje(db.Model):
    __tablename__ = 'personaje'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.String(250))
    altura = db.Column(db.Integer)
    genero = db.Column(db.String(50))
    personajes_favoritos = relationship('PersonajeFavorito', back_populates='personaje', cascade='all,delete')


    def __repr__(self):
        return '<Personaje %r>' % self.nombre

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "altura": self.altura,
            "genero": self.genero
            # do not serialize the password, its a security breach
        }
    
class PlanetaFavorito(db.Model):
    __tablename__ = 'planeta_favorito'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    planeta_id = db.Column(db.Integer, db.ForeignKey('planeta.id'))
    usuario = relationship('Usuario', back_populates='planetas_favoritos')
    planeta = relationship('Planeta', back_populates='planetas_favoritos')

class PersonajeFavorito(db.Model):
    __tablename__ = 'personaje_favorito'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    personaje_id = db.Column(db.Integer, db.ForeignKey('personaje.id'))
    usuario = relationship('Usuario', back_populates='personajes_favoritos')
    personaje = relationship('Personaje', back_populates='personajes_favoritos')
