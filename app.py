# -----------------------------------------------------------------------------
# Versão em Português:
# Este código implementa uma aplicação Flask para gerenciar diversos aspectos 
# do universo Star Wars, como personagens, filmes, planetas, espaçonaves, espécies, 
# veículos e favoritos. Ele utiliza SQLAlchemy para interagir com um banco de dados 
# SQLite e organiza suas rotas através de Blueprints, permitindo uma estrutura 
# modular e organizada do código.
#
# English Version:
# This code implements a Flask application to manage various aspects of the Star 
# Wars universe, such as characters, movies, planets, starships, species, vehicles, 
# and favorites. It uses SQLAlchemy to interact with a SQLite database and organizes 
# its routes through Blueprints, allowing for a modular and organized structure.
#
# Copyright © 2024 Jeremias Nunes. All rights reserved.
# Copyright © 2024 Rafael Mesquita. All rights reserved.
# -----------------------------------------------------------------------------

from flask import Flask, jsonify, render_template
from models import db  # Importação do db

# Importação dos Blueprints
from Routes.character_routes import character_bp
from Routes.movie_routes import movie_bp
from Routes.planet_routes import planet_bp
from Routes.starship_routes import starship_bp
from Routes.species_routes import species_bp
from Routes.vehicle_routes import vehicle_bp
from Routes.favorite_routes import favorite_bp

# Função para criar a aplicação Flask
def create_app():
    app = Flask(__name__)
    
    # Configuração do banco de dados SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicialização do banco de dados
    db.init_app(app)

    # Registro dos Blueprints para rotas
    app.register_blueprint(character_bp)
    app.register_blueprint(movie_bp)
    app.register_blueprint(planet_bp)
    app.register_blueprint(starship_bp)
    app.register_blueprint(species_bp)
    app.register_blueprint(vehicle_bp)
    app.register_blueprint(favorite_bp)

    return app

# Criação da aplicação
app = create_app()

# Rota principal que renderiza o template HTML
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# Rota para listar os endpoints em formato JSON
@app.route('/endpoints', methods=['GET'])
def list_endpoints():
    endpoints = {}
    
    # Itera sobre todas as rotas registradas no Flask
    for rule in app.url_map.iter_rules():
        endpoints[rule.endpoint] = {
            "methods": list(rule.methods),
            "url": str(rule)
        }
    
    # Retorna a lista de endpoints em formato JSON
    return jsonify(endpoints)

# Criação do banco de dados no contexto da aplicação
with app.app_context():
    db.create_all()

# Executa a aplicação no modo debug
if __name__ == '__main__':
    app.run(debug=True)
