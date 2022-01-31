from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


starshipfavourites = db.Table('starshipfavourites',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('starship_id', db.Integer, db.ForeignKey('starship.id'), primary_key=True))
                              
speciesfavourites = db.Table('speciesfavourites',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('species_id', db.Integer, db.ForeignKey('species.id'), primary_key=True))

favourite_character= db.Table('favourite_character',
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("people_id", db.Integer, db.ForeignKey("people.id"), primary_key=True))

class User(db.Model):
    __tablename__: 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    _password = db.Column(db.String(1000), unique=False, nullable=False)
    _is_active = db.Column(db.Boolean(), unique=False, nullable=False, default=True)

    have_user_species = db.relationship('Species', secondary = speciesfavourites, back_populates="have_user_speciesfav")

    have_char = db.relationship("People", secondary=favourite_character, back_populates="have_user")
                              
    have_user_starship = db.relationship('Starship', secondary=starshipfavourites, back_populates="have_user_starshipfav")

    def __repr__(self):
        return f'User is {self.username}, with {self.email} and {self.id}'
    

    def to_dict(self):
        return {
            "id": self.id,
            "username":self.username,
            "email": self.email,
            "starships": [starship.to_dict() for starship in self.have_user_starship],
            "species": [species.to_dict() for species in self.have_user_species],
            "characters": [people.to_dict() for people in self.have_char] 
        }

    def create(self):
       db.session.add(self)
       db.session.commit()


    @classmethod
    def get_by_email(cls, email):
        account = cls.query.filter_by(email=email).one_or_none()
        return account


    @classmethod
    def get_by_password(cls, password):
        secretPass = cls.query.filter_by(password=password).one_or_none()
        return secretPass

    @classmethod
    def get_all(cls):
        users = cls.query.all()
        return users
  

    @classmethod
    def get_by_id(cls, id):
        user_id = cls.query.get(id)
        return user_id


    def add_fav_starship (self,starship):
        self.have_user_starship.append(starship)
        return self.have_user_starship


class Starship(db.Model):
    __tablename__ : 'starship'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    starships_id = db.Column(db.Integer, db.ForeignKey("starship_detail.id"), nullable=False)

    starship_has_details = db.relationship("StarshipDetail", back_populates = "starship_detail_has_starship")
    have_user_starshipfav = db.relationship("User", secondary=starshipfavourites, back_populates = "have_user_starship")
    

    def __repr__(self):
        return f'Starship is starships_id:{self.starship_id}, id:{self.id}, name:{self.name}'

    def to_dict(self):
        return {
            "id": self.id,
            "name":self.name,
            "starships_id": self.starships_id
            # do not serialize the password, its a security breach
        }
    @classmethod
    def get_all(cls):
        starships = cls.query.all()
        return starships

    @classmethod
    def get_by_id(cls, id):
        starship_id = cls.query.get(id)
        return starship_id

class StarshipDetail(db.Model):
    __tablename__ : 'starship_detail'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    model = db.Column(db.Integer, unique=False, nullable=False)
    starship_class = db.Column(db.String(120), unique=False, nullable=False)
    manufacturer = db.Column(db.String(120), unique=False, nullable=False)
    

    starship_detail_has_starship = db.relationship("Starship", back_populates = "starship_has_details")

    def __repr__(self):
        return f'StarshipDetail is id:{self.id}, name: {self.name}, model: {self.model}, starship_class: {self.starship_class}, manufacturer:{self.manufacturer}'

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "starship_class": self.starship_class,
            "manufacturer": self.manufacturer,
        }

@classmethod
def get_by_id(cls, id):
    starship = cls.query.get(id)
    return starship
                              
    @classmethod
    def get_user_by_id(cls,id):
        user = cls.query.get(id)
        return user
    
    def add_fav_species(self,specie):
        self.have_user_species.append(specie)
        db.session.commit()
        return self.have_user_species
    
    def new_fav_people (self,people):
        self.have_char.append(people)
        db.session.commit()
        return self.have_char


class Species(db.Model):
    __tablename__:"species"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=False, nullable=False)
    species_id = db.Column(db.Integer, db.ForeignKey("species_details.id"), nullable=False)

    species_have = db.relationship("SpeciesDetails", back_populates = "species_have_details")
    have_user_speciesfav= db.relationship('User', secondary= speciesfavourites, back_populates="have_user_species")

    def __repr__(self):
        return f'Species: {self.id}, name: {self.name}'

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }
        
    @classmethod    
    def get_all(cls):
        species = cls.query.all()
        return species

    @classmethod
    def get_by_id(cls, id):
        species = cls.query.get(id)
        return species
                              
class People(db.Model):
    __tablename__: "people"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=False, nullable=False)
    detail_id = db.Column(db.Integer, db.ForeignKey("people_detail.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    people_has_details = db.relationship("PeopleDetail", back_populates="detail_has_character")
    have_user = db.relationship("User", secondary=favourite_character, back_populates="have_char")


    def __repr__(self):
        return f'People is {self.name}, url: {self.url}'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

    @classmethod
    def get_all(cls):
        character_list = cls.query.all()
        return character_list


    @classmethod
    def get_by_id(cls, id):
        character = cls.query.get(id)
        return character
       
                        
class SpeciesDetails(db.Model):
    __tablename__:"species_details"

    id = db.Column(db.Integer, primary_key=True)
    classification = db.Column(db.String(250), unique=False, nullable=False)
    designation = db.Column(db.String(250),unique=False, nullable=False)
    average_height = db.Column(db.Integer, unique=False, nullable=False)
    average_lifespan = db.Column(db.Integer, unique=False, nullable=False)
    hair_color = db.Column(db.String(250), unique=False, nullable=False)
    eye_color = db.Column(db.String(250), unique=False, nullable=False)
    homeworld = db.Column(db.String(250), unique=False, nullable=False)
    language = db.Column(db.String(250), unique=False, nullable=False)
    people = db.Column(db.String(250), unique=False, nullable=False)
    name = db.Column(db.String(250), unique=False, nullable=False)

    species_have_details = db.relationship('Species', back_populates="species_have")

    def __repr__(self):
        return f'SpeciesDetails is {self.classificacion}, classification:{self.classificacion}, designation:{self.designation}, average_height:{average_height}, average_lifespan:{self.average_lifespan}, hair_color:{self.hair_color}, eye_color:{self.eye_color}, homeworld:{self.homeworld}, language:{self.language}, people:{self.people}, name:{self.name}' 
        
    def to_dict(self):
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
            "edited": self.edited,
            "name": self.name,
        }
    
    @classmethod
    def get_all_speciesdetails(cls):
        speciesdetails = cls.query.all()
        return speciesdetails
    
    @classmethod
    def get_by_id_speciesdetails(cls,id):
        speciesdetails = cls.query.get(id)
        return speciesdetails
   

class PeopleDetail(db.Model):
    __tablename__: "people_detail" 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=False, nullable=False)
    eye_color = db.Column(db.String(250), unique=False, nullable=False)
    gender = db.Column(db.String(250), unique=False, nullable=False)
    homeworld = db.Column(db.String(250), unique=False, nullable=False)

    detail_has_character = db.relationship("People", back_populates="people_has_details")

    # def __repr__(self):
    #     return '<PeopleDetail>' % self.username


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "created": self.created,
            "edited": self.edited,
            "homeworld": self.homeworld
        }
