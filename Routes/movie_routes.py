# -----------------------------------------------------------------------------
# Versão em Português:
# Este código implementa um serviço web para gerenciar filmes da franquia Star Wars. 
# Ele permite listar, adicionar, excluir e buscar filmes da base de dados local, 
# bem como buscar filmes diretamente da API SWAPI. Utiliza Flask como framework web 
# e SQLAlchemy para manipulação do banco de dados.

# English Version:
# This code implements a web service for managing Star Wars movies. 
# It allows listing, adding, deleting, and fetching movies from the local database, 
# as well as retrieving movies directly from the SWAPI API. It uses Flask as the 
# web framework and SQLAlchemy for database handling.

# Copyright © 2024 Jeremias Nunes. All rights reserved.
# Copyright © 2024 Rafael Mesquita. All rights reserved.
# -----------------------------------------------------------------------------

from flask import Blueprint, abort, jsonify, request
from models import db, Movie
import requests
import json
from datetime import datetime

# Criação do Blueprint
movie_bp = Blueprint('movies', __name__)

# Função auxiliar para salvar um novo registro
def save_record(model, data):
    new_record = model(**data)
    db.session.add(new_record)
    db.session.commit()
    return new_record

# Função auxiliar para carregar/deserializar JSON
def load_json(value):
    try:
        return json.loads(value) if value else []
    except json.JSONDecodeError:
        return []

# Função auxiliar para buscar dados de uma API externa (SWAPI)
def fetch_from_swapi(endpoint):
    try:
        response = requests.get(f"https://swapi.dev/api/{endpoint}/")
        response.raise_for_status()  # Verifica se houve erro na resposta
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching from SWAPI: {e}")
        return None

# Função para buscar filmes da SWAPI e salvar no banco de dados
def fetch_and_save_films():
    swapi_data = fetch_from_swapi('films')
    if swapi_data:
        for item in swapi_data['results']:
            print(f"Processing movie: {item['title']}")
            try:
                # Convert the release_date from string to a Python date object
                release_date = datetime.strptime(item["release_date"], "%Y-%m-%d").date()

                movie_data = {
                    "title": item["title"],
                    "episode_id": item["episode_id"],
                    "opening_crawl": item["opening_crawl"],
                    "director": item["director"],
                    "producer": item["producer"],
                    "release_date": release_date,
                    "characters": json.dumps([]),
                    "planets": json.dumps([]),
                    "starships": json.dumps([]),
                    "vehicles": json.dumps([]),
                    "species": json.dumps([])
                }
                
                # Evitar duplicatas
                if not Movie.query.filter_by(title=movie_data['title']).first():
                    save_record(Movie, movie_data)
                    print(f"Saved movie: {movie_data['title']}")
            except Exception as e:
                print(f"Falha ao salvar filme {item['title']}: {str(e)}")
    else:
        print("No data fetched from SWAPI.")

# Rota para listar todos os filmes e salvar dados da API SWAPI
@movie_bp.route('/filmes', methods=['GET'])
def get_filmes():
    if not Movie.query.first():
        fetch_and_save_films()
    
    filmes_list = Movie.query.all()
    result = [{
        "id": f.id,
        "title": f.title,
        "episode_id": f.episode_id,
        "opening_crawl": f.opening_crawl,
        "director": f.director,
        "producer": f.producer,
        "release_date": f.release_date,
        "characters": load_json(f.characters),
        "planets": load_json(f.planets),
        "starships": load_json(f.starships),
        "vehicles": load_json(f.vehicles),
        "species": load_json(f.species)
    } for f in filmes_list]
    return jsonify(result)

# Rota para buscar um filme específico pelo ID
@movie_bp.route('/filmes/<int:id>', methods=['GET'])
def get_filme(id):
    f = Movie.query.get(id)
    if not f:
        abort(404, description="filme não encontrado")

    return jsonify({
        "id": f.id,
        "title": f.title,
        "episode_id": f.episode_id,
        "opening_crawl": f.opening_crawl,
        "director": f.director,
        "producer": f.producer,
        "release_date": f.release_date,
        "characters": load_json(f.characters),
        "planets": load_json(f.planets),
        "starships": load_json(f.starships),
        "vehicles": load_json(f.vehicles),
        "species": load_json(f.species)
    })

# Rota para adicionar um novo filme manualmente ao banco de dados
@movie_bp.route('/filmes', methods=['POST'])
def save_filme():
    data = request.json
    try:
        # Convertendo campos para JSON quando necessário
        data['characters'] = json.dumps(data.get('characters', []))
        data['planets'] = json.dumps(data.get('planets', []))
        data['starships'] = json.dumps(data.get('starships', []))
        data['vehicles'] = json.dumps(data.get('vehicles', []))
        data['species'] = json.dumps(data.get('species', []))

        # Converte a data de lançamento para objeto datetime
        data['release_date'] = datetime.strptime(data['release_date'], "%Y-%m-%d").date()

        new_filme = save_record(Movie, data)
        return jsonify({"message": "Filme salvo com sucesso!", "id": new_filme.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Rota para deletar um filme pelo ID
@movie_bp.route('/filmes/<int:id>', methods=['DELETE'])
def delete_filme(id):
    f = Movie.query.get(id)
    if not f:
        return jsonify({"error": "Filme não encontrado"}), 404

    db.session.delete(f)
    db.session.commit()
    return jsonify({"message": "Filme deletado com sucesso!"})
