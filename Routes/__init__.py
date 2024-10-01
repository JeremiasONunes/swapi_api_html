# -----------------------------------------------------------------------------
# Versão em Português:
# Este módulo configura e cria uma aplicação Flask que interage com um banco 
# de dados SQLite e organiza suas rotas em Blueprints, modularizando o gerenciamento 
# de recursos do universo Star Wars, como personagens, filmes, planetas, 
# espaçonaves, espécies, veículos e favoritos.
#
# English Version:
# This module configures and creates a Flask application that interacts with 
# a SQLite database and organizes its routes into Blueprints, modularizing 
# the management of Star Wars universe resources, such as characters, movies, 
# planets, starships, species, vehicles, and favorites.
#
# Copyright © 2024 Jeremias Nunes. All rights reserved.
# Copyright © 2024 Rafael Mesquita. All rights reserved.
# -----------------------------------------------------------------------------

from flask import Flask
from models import db  # Importa o objeto db para interagir com o banco de dados

# Função que cria e configura a aplicação Flask
def create_app():
    app = Flask(__name__)

    # Configurações da aplicação, incluindo o banco de dados SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Modifique o caminho conforme necessário
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa o banco de dados com a aplicação
    db.init_app(app)

    # Registro dos Blueprints das rotas da aplicação

    from .character_routes import character_bp  # Importa o blueprint de personagens
    app.register_blueprint(character_bp)

    from .movie_routes import movie_bp  # Importa o blueprint de filmes
    app.register_blueprint(movie_bp)

    from .planet_routes import planet_bp  # Importa o blueprint de planetas
    app.register_blueprint(planet_bp)

    from .starship_routes import starship_bp  # Importa o blueprint de espaçonaves
    app.register_blueprint(starship_bp)

    from .species_routes import species_bp  # Importa o blueprint de espécies
    app.register_blueprint(species_bp)

    from .vehicle_routes import vehicle_bp  # Importa o blueprint de veículos
    app.register_blueprint(vehicle_bp)

    from .favorite_routes import favorite_bp  # Importa o blueprint de favoritos
    app.register_blueprint(favorite_bp)

    return app

# O padrão de execução do aplicativo (como o app.run()) deve ser implementado 
# em outro arquivo, como app.py, para separar a lógica de inicialização do código.
