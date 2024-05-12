from . import db

class CatForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cat_name = db.Column(db.String(100), nullable=False)
    cat_photo = db.Column(db.String(255), nullable=True)
    cat_age = db.Column(db.Integer, nullable=False)
    cat_breed = db.Column(db.String(100), nullable=False)
    cat_gender = db.Column(db.String(10), nullable=False)
    cat_neutered = db.Column(db.String(10), nullable=False)
    cat_vaccine = db.Column(db.String(10), nullable=False)
    cat_special_needs = db.Column(db.String(100), nullable=False)
    cat_about_me = db.Column(db.String(200), nullable=False)
    owner_name = db.Column(db.String(100), nullable=False)
    owner_email = db.Column(db.String(100), nullable=False)
    owner_contact = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"CatForm('{self.cat_name}','{self.cat_photo}', '{self.cat_age}','{self.cat_breed}','{self.cat_gender}','{self.cat_neutered}','{self.cat_vaccine}','{self.cat_special_needs}','{self.cat_about_me}','{self.owner_name}','{self.owner_email}', '{self.owner_contact}')"
