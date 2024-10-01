from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import CheckConstraint

db = SQLAlchemy()

class Character(db.Model):
    __tablename__ = 'characters'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    height = db.Column(db.Float, nullable=True)
    mass = db.Column(db.Float, nullable=True)
    hair_color = db.Column(db.String(20), nullable=True)
    skin_color = db.Column(db.String(20), nullable=True)
    eye_color = db.Column(db.String(20), nullable=True)
    birth_year = db.Column(db.String(20), nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    homeworld = db.Column(db.String(100), nullable=True)
    films = db.Column(db.Text, nullable=True)  # Store as JSON
    species = db.Column(db.Text, nullable=True)  # Store as JSON
    vehicles = db.Column(db.Text, nullable=True)  # Store as JSON
    starships = db.Column(db.Text, nullable=True)  # Store as JSON
    created = db.Column(db.DateTime, default=datetime.utcnow)  # Track creation time
    edited = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Track last edit time

    def __repr__(self):
        return f'<Character(name={self.name}, height={self.height}, mass={self.mass})>'
    
    

# Model for Movie
class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    episode_id = db.Column(db.Integer, nullable=False)
    opening_crawl = db.Column(db.Text, nullable=False)
    director = db.Column(db.String, nullable=False)
    producer = db.Column(db.String, nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    characters = db.Column(db.Text, nullable=False)  # Armazena URLs como texto
    planets = db.Column(db.Text, nullable=False)      # Armazena URLs como texto
    starships = db.Column(db.Text, nullable=False)    # Armazena URLs como texto
    vehicles = db.Column(db.Text, nullable=False)     # Armazena URLs como texto
    species = db.Column(db.Text, nullable=False)      # Armazena URLs como texto
    created = db.Column(db.DateTime, default=datetime.utcnow)
    edited = db.Column(db.DateTime, onupdate=datetime.utcnow)

    @property
    def url(self):
        return f'https://swapi.dev/api/films/{self.id}/'

    def __repr__(self):
        return f'<Movie {self.title}>'
# Model for Planet
class Planet(db.Model):
    __tablename__ = 'planets'
    
    id = db.Column(db.Integer, primary_key=True)  # ID da API
    name = db.Column(db.String(100), nullable=False)
    rotation_period = db.Column(db.Integer, nullable=True)
    orbital_period = db.Column(db.Integer, nullable=True)
    diameter = db.Column(db.Integer, nullable=True)
    climate = db.Column(db.String(100), nullable=True)
    gravity = db.Column(db.String(100), nullable=True)
    terrain = db.Column(db.String(100), nullable=True)
    surface_water = db.Column(db.Integer, nullable=True)
    population = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f'<Planet(name={self.name}, population={self.population})>'


# Model for Starship
class Starship(db.Model):
    __tablename__ = 'starships'
    
    id = db.Column(db.Integer, primary_key=True)  # ID da API
    name = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=True)
    manufacturer = db.Column(db.String(100), nullable=True)
    cost_in_credits = db.Column(db.Integer, CheckConstraint('cost_in_credits >= 0'), nullable=True)
    length = db.Column(db.Float, CheckConstraint('length >= 0'), nullable=True)
    max_atmosphering_speed = db.Column(db.Integer, nullable=True)  # Alterado para Integer
    crew = db.Column(db.Integer, nullable=True)  # Alterado para Integer
    passengers = db.Column(db.Integer, nullable=True)  # Alterado para Integer
    cargo_capacity = db.Column(db.Integer, CheckConstraint('cargo_capacity >= 0'), nullable=True)  # Alterado para Integer
    consumables = db.Column(db.String(100), nullable=True)
    hyperdrive_rating = db.Column(db.Float, nullable=True)  # Alterado para Float
    MGLT = db.Column(db.Integer, nullable=True)  # Alterado para Integer
    starship_class = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<Starship(name={self.name}, model={self.model})>'
    
    def to_dict(self):
        """Return a dictionary representation of the Starship for JSON serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "crew": self.crew,
            "passengers": self.passengers,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
            "hyperdrive_rating": self.hyperdrive_rating,
            "MGLT": self.MGLT,
            "starship_class": self.starship_class
        }

# Model for Species
class Species(db.Model):
    __tablename__ = 'species'
    
    id = db.Column(db.Integer, primary_key=True)  # ID da API
    name = db.Column(db.String(100), nullable=False)
    classification = db.Column(db.String(100), nullable=True)
    designation = db.Column(db.String(100), nullable=True)
    average_height = db.Column(db.Float, nullable=True)
    skin_colors = db.Column(db.String(100), nullable=True)
    hair_colors = db.Column(db.String(100), nullable=True)
    eye_colors = db.Column(db.String(100), nullable=True)
    average_lifespan = db.Column(db.Integer, nullable=True)
    homeworld = db.Column(db.String(100), nullable=True)
    language = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<Species(name={self.name}, average_height={self.average_height})>'


class Vehicle(db.Model):
    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    model = db.Column(db.String(100))
    manufacturer = db.Column(db.String(100))
    cost_in_credits = db.Column(db.String(20))
    length = db.Column(db.String(20))
    max_atmosphering_speed = db.Column(db.String(20))
    crew = db.Column(db.String(20))
    passengers = db.Column(db.String(20))
    cargo_capacity = db.Column(db.String(20))
    consumables = db.Column(db.String(20))
    vehicle_class = db.Column(db.String(50))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    edited = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
# Model for Favorites
class Favorite(db.Model):
    __tablename__ = 'favorites'
    
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, nullable=False)
    movie_id = db.Column(db.Integer, nullable=True)
    starship_id = db.Column(db.Integer, nullable=True)
    vehicle_id = db.Column(db.Integer, nullable=True)
    species_id = db.Column(db.Integer, nullable=True)
    planet_id = db.Column(db.Integer, nullable=True)
    student_name1 = db.Column(db.String(100), nullable=False)
    registration1 = db.Column(db.String(50), nullable=False)
    student_name2 = db.Column(db.String(100), nullable=True)
    registration2 = db.Column(db.String(50), nullable=True)
    course = db.Column(db.String(100), nullable=False)
    university = db.Column(db.String(100), nullable=False)
    period = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Favorite(character_id={self.character_id})>'