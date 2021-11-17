from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nick = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    

    def __repr__(self):
        return f'User {self.email}'

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password
        }
    
    def get_all():
        users = query.all()
        return users
    
class Species(db.Model):
    __tablename__:"species"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False, nullable=False)
    detail_id = db.Column(db.Integer, db.ForeignKey("species_details.id"), nullable=False)

    people_has_detail = db.relationship("SpeciesDetails", back_populates="detail_has_specie")

    
    def repr(self):
        return f'Species: {self.id}, url: {self.url}'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }

    @classmethod    
    def get_all(cls):
        species_list = cls.query.all()
        return [species.serialize() for i in species_list]

    @classmethod
    def get_by_id(cls, id):
        specie = cls.query.get(id)
        return specie


class SpeciesDetails(db.Model):
    __tablename__:"species_details"
    id = db.Column(db.Integer, primary_key=True)
    classification = db.Column(db.String(250), unique=False, nullable=False)
    designation = db.Column(db.String(250),unique=False, nullable=False)
    average_height = db.Column(db.FLOAT, unique=False, nullable=False)
    average_lifespan = db.Column(db.Integer, unique=False, nullable=False)
    hair_color = db.Column(db.String(250), unique=False, nullable=False)
    eye_color = db.Column(db.String(250), unique=False, nullable=False)
    homeworld = db.Column(db.String(250), unique=False, nullable=False)
    language = db.Column(db.String(250), unique=False, nullable=False)
    people = db.Column(db.String(250), unique=False, nullable=False)
    created = db.Column(db.DATETIME(250), unique=False, nullable=False)
    edited = db.Column(db.DATETIME(250), unique=False, nullable=False)
    name = db.Column(db.String(250), unique=False, nullable=False)

    detail_has_specie = db.relationship("Species", back_populates="people_has_detail")
    #people_has_detail = db.relationship("SpeciesDetails", back_populates="detail_has_specie")

    """ def __repr__(self):
        return "<SpeciesDetails>" % self.username """
        
    def serialize(self):
        return {
            "id" : self.id,
            "classificacion": self.classificacion,
            "designation": self.designation,
            "average_height": self.average_height,
            "average_lifespan": self.average_lifespan,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
            "homeworld": self.homeworld,
            "language": self.language,
            "people": self.people,
            "created": self.created,
            "edited": self.edited,
            "name": self.name,
        }
   
     