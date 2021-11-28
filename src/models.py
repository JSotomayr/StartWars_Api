from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

starshipfavourites = db.Table('starshipfavourites',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('starship_id', db.Integer, db.ForeignKey('starship.id'), primary_key=True)
)

class User(db.Model):
    __tablename__: 'user'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(250), unique = True, nullable = False)
    email = db.Column(db.String(250), unique = True, nullable = False)
    _password = db.Column(db.String(250), unique = True, nullable = False)
    _is_active = db.Column(db.String(250), unique = True, nullable = False, default = True)

    have_user_starship = db.relationship('Starship', secondary=starshipfavourites, back_populates="have_user_starshipfav")

    def __repr__(self):
        return f'User is id:{self.d}, email:{self.email}, username:{self.username}, _password:{self.password}, _is_active:{self._is_active}'

    def to_dict(self):
        return {
            "id": self.id,
            "username":self.username,
            "email": self.email,
            "starships": [starship.to_dict() for starship in self.have_user_starship]
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
        return f'StarshipDetail is id:{self.id}, name: {self.name}, model: {self.model}, starship_class: {self.starship_class}, manufacturer:{self.manufacturer}, cost_in_credits:{self.cost_in_credits}, length:{self.length}, max_atmosphering_speed:{self.max_atmosphering_speed}, crew:{self.crew}, passengers:{self.passengers}, pilots:{self.pilots}, cargo_capacity:{self.cargo_capacity}, consumables:{self.consumables}, hyperdrive_rating:{self.hyperdrive_rating}, mlgt:{self.mlgt}, pilots:{self.films}, films:{self.films}, created:{self.created}, edited:{self.edited}, url:{self.url}'

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
