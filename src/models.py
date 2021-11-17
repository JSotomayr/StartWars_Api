from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__: 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    _password = db.Column(db.String(80), unique=False, nullable=False)
    _is_active = db.Column(db.Boolean(), unique=False, nullable=False, default=True)

    def __repr__(self):
        return f'User is {self.username}, with {self.email} and {self.id}'
    

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username
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


class Favourite(db.Model):
    __tablename__: "favourite"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


    @classmethod
    def get_all(cls):
        favourite = cls.query.all()
        return favourite


class FavouritePeople(db.Model):
    __tablename__: "favourite_people"

    id = db.Column(db.Integer, primary_key=True)
    people_id = db.Column(db.Integer, db.ForeignKey("people.id"), nullable=False)


class People(db.Model):
    __tablename__: "people"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=False, nullable=False)
    detail_id = db.Column(db.Integer, db.ForeignKey("people_detail.id"), nullable=False)

    people_has_details = db.relationship("PeopleDetail", back_populates="detail_has_character")

    def __repr__(self):
        return f'People is {self.name}, url: {self.url}'

    def to_dict(self):
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


class PeopleDetail(db.Model):
    __tablename__: "people_detail" 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=False, nullable=False)
    height = db.Column(db.FLOAT, unique=False, nullable=False)
    mass = db.Column(db.FLOAT, unique=False, nullable=False)
    hair_color = db.Column(db.String(250), unique=False, nullable=False)
    skin_color = db.Column(db.String(250), unique=False, nullable=False)
    eye_color = db.Column(db.String(250), unique=False, nullable=False)
    birth_year = db.Column(db.DATETIME(timezone=False), unique=False, nullable=False) 
    gender = db.Column(db.String(250), unique=False, nullable=False)
    created = db.Column(db.DATETIME(timezone=False), unique=False, nullable=False)
    edited =db.Column(db.DATETIME(timezone=False), unique=False, nullable=False)
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


        