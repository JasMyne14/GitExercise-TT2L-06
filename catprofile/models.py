from flask_sqlalchemy import SQLAlchemy
from . import db


class CatForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    breed = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    neutered = db.Column(db.String(10), nullable=False)
    vaccine = db.Column(db.String(10), nullable=False)
    special_needs = db.Column(db.String(100), nullable=False)
    about_me = db.Column(db.String(200), nullable=False)
    owner_name = db.Column(db.String(100), nullable=False)
    owner_email = db.Column(db.String(100), nullable=False)
    owner_contact = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"CatForm('{self.name}', '{self.age}','{self.breed}','{self.gender}','{self.neutered}','{self.vaccine}','{self.special_needs}','{self.about_me}','{self.owner_name}','{self.owner_email}', '{self.owner_contact}')"
