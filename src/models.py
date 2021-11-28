from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

#               ASSOCIATION TABLE: TABLA FAVORITES

favourites = db.Table('favourites', 
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('planet_id', db.Integer, db.ForeignKey('planet.id'))
)

#                           USER
class User(db.Model):
    __tablename__: 'user'

    id = db.Column(db.Integer, primary_key=True,)
    username = db.Column(db.String(250), unique=True, nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    _password = db.Column(db.String(250), unique=True, nullable=False)
    _is_active = db.Column(db.String(250), unique=True, nullable=False, default = True)

#       RELACION USER Y FAVORITOS

    have_planets = db.relationship(
        "Planet",
        secondary= favourites,
        back_populates="have_users")



    def __repr__(self):
        return f'User is id:{self.id}, username:{self.username}, email:{self.email}, _password{self._password}, _is_active{self._is_active}'

    def to_dict(self):
        return {
        "id" : self.id, 
        "username" : self.username, 
        "email" : self.email, 

        #                       DICCIONARIO FAV 
        "Favplanets" : [planet.to_dict() for planet in self.have_planets]

        }

    

#                           POST create user

    def create(self):
        db.session.add(self)
        db.session.commit()


#                           POST email y password

    @classmethod
    def get_by_email(cls, email):
        account = cls.query.filter_by(email=email).one_or_none()
        return account

    @classmethod
    def get_by_password(cls, password):
        secretPass = cls.query.filter_by(password=password).one_or_none()
        return secretPass



#                           GET user 
    @classmethod
    def get_all(cls):
        users = cls.query.all()
        return users

#                       GETplanet
    @classmethod
    def get_by_id(cls,id):
        user_id = cls.query.get(id)
        return user_id

#                       GET user ID
    @classmethod
    def get_by_id_user(cls,id_user):
        user = cls.query.filter_by(id=id_user).one_or_none()
        return user


#                       GET favoritos Planet                 
    def add_fav_planet (self,planet):
        self.have_planets.append(planet)
        db.session.commit()
        return self.have_planets


#                           PLANET

class Planet(db.Model):
    __tablename__: 'planet'

    id = db.Column(db.Integer, primary_key=True, )
    planet_name = db.Column(db.String(250), unique=False, nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey("planet_detail.id"), nullable=False)

    planet_has_planet_details = db.relationship("PlanetDetail", back_populates = "planet_detail_has_planet")

#          Relacion favorito usuario
    have_users = db.relationship(
        "User",
        secondary=favourites,
        back_populates="have_planets")


    def __repr__(self):
        return f'Planet is id:{self.id}, planet_name:{self.planet_name}, planet_id:{self.planet_id}'

    def to_dict(self):
        return {
            "id": self.id,
            "planet_name": self.planet_name,

        }

#                           get Planet
    @classmethod
    def get_all_planets(cls):
        planets = cls.query.all()
        return planets


#                           get planet id

# porque es la primary key, no necesita filter
    @classmethod
    def get_by_id(cls, id): 
        planet = cls.query.get(id)
        return planet

#                           PLANET ID

class PlanetDetail(db.Model):
    __tablename__: 'planet_detail'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=False, nullable=False)
    diameter = db.Column(db.Integer, unique=False, nullable=False)

    planet_detail_has_planet = db.relationship("Planet", back_populates = "planet_has_planet_details")

    def __repr__(self):
        return f'PlanetDetail is name:{self.name}, id:{self.id},"diameter": {self.diameter}'

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.id,
            "diameter": self.diameter,
        }

    







