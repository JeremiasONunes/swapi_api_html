# -----------------------------------------------------------------------------
# Versão em Português:
# Este código implementa um serviço web para gerenciar espécies da franquia 
# Star Wars. Ele permite listar, adicionar, excluir e buscar espécies na base 
# de dados local, bem como buscar espécies diretamente da API SWAPI. Utiliza 
# Flask como framework web e SQLAlchemy para manipulação do banco de dados.

# English Version:
# This code implements a web service for managing species from the Star Wars 
# franchise. It allows listing, adding, deleting, and fetching species from the 
# local database, as well as retrieving species directly from the SWAPI API. 
# Flask is used as the web framework, and SQLAlchemy is used for database handling.

# Copyright © 2024 Jeremias Nunes. All rights reserved.
# Copyright © 2024 Rafael Mesquita. All rights reserved.
# -----------------------------------------------------------------------------

from flask import Blueprint, jsonify, request, abort
import requests
import json
from models import db, Species

# Criação do Blueprint
species_bp = Blueprint('species', __name__)

# Função auxiliar para salvar um novo registro
def save_record(model, data):
    new_record = model(**data)
    db.session.add(new_record)
    db.session.commit()
    return new_record

# Função auxiliar para deserializar JSON
def load_json(value):
    try:
        return json.loads(value) if value else []
    except json.JSONDecodeError:
        return []

# Função auxiliar para buscar dados da SWAPI
def fetch_from_swapi(endpoint):
    try:
        response = requests.get(f"https://swapi.dev/api/{endpoint}/")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching from SWAPI: {e}")
        return None

# Função auxiliar para converter valores não numéricos para None
def convert_to_float(value):
    try:
        if value.lower() == 'n/a':
            return None
        return float(value)
    except (ValueError, AttributeError):
        return None

# Função para buscar todas as páginas de espécies da SWAPI e salvar no banco de dados
def fetch_and_save_species():
    url = 'https://swapi.dev/api/species/'
    while url:
        response = requests.get(url)
        if response.status_code == 200:
            swapi_data = response.json()
            if swapi_data and 'results' in swapi_data:
                for item in swapi_data['results']:
                    species_data = {
                        "name": item["name"],
                        "classification": item.get("classification"),
                        "designation": item.get("designation"),
                        "average_height": convert_to_float(item.get("average_height")),
                        "skin_colors": json.dumps(item.get("skin_colors", [])),
                        "hair_colors": json.dumps(item.get("hair_colors", [])),
                        "eye_colors": json.dumps(item.get("eye_colors", [])),
                        "average_lifespan": convert_to_float(item.get("average_lifespan")),
                        "language": item.get("language"),
                        "homeworld": item.get("homeworld")  # Caso o campo esteja no banco
                    }
                    try:
                        # Evitar duplicatas: verifica se a espécie já está salva
                        if not Species.query.filter_by(name=species_data['name']).first():
                            save_record(Species, species_data)
                    except Exception as e:
                        print(f"Falha ao salvar espécie {item['name']}: {str(e)}")
            
            # Atualiza a URL para a próxima página
            url = swapi_data.get('next')
        else:
            print(f"Erro ao acessar a SWAPI: {response.status_code}")
            break

# Rota para listar todas as espécies (e buscar da SWAPI se o banco de dados estiver vazio)
@species_bp.route('/especies', methods=['GET'])
def get_species():
    # Verifica se há espécies no banco de dados local, caso contrário busca da SWAPI
    if not Species.query.first():
        fetch_and_save_species()

    # Agora busca todas as espécies do banco de dados
    species_list = Species.query.all()
    result = [{
        "id": s.id,
        "name": s.name,
        "classification": s.classification,
        "designation": s.designation,
        "average_height": s.average_height,
        "skin_colors": load_json(s.skin_colors),
        "hair_colors": load_json(s.hair_colors),
        "eye_colors": load_json(s.eye_colors),
        "average_lifespan": s.average_lifespan,
        "language": s.language
    } for s in species_list]

    return jsonify(result)

# Rota para retornar uma espécie específica pelo ID
@species_bp.route('/especies/<int:id>', methods=['GET'])
def get_species_by_id(id):
    s = Species.query.get(id)
    if not s:
        abort(404, description="Espécie não encontrada")

    return jsonify({
        "id": s.id,
        "name": s.name,
        "classification": s.classification,
        "designation": s.designation,
        "average_height": s.average_height,
        "skin_colors": load_json(s.skin_colors),
        "hair_colors": load_json(s.hair_colors),
        "eye_colors": load_json(s.eye_colors),
        "average_lifespan": s.average_lifespan,
        "language": s.language
    })

# Rota para salvar uma nova espécie no banco de dados
@species_bp.route('/especies', methods=['POST'])
def save_species():
    data = request.json
    try:
        # Converte os campos que precisam ser armazenados como JSON
        data['skin_colors'] = json.dumps(data.get('skin_colors', []))
        data['hair_colors'] = json.dumps(data.get('hair_colors', []))
        data['eye_colors'] = json.dumps(data.get('eye_colors', []))
        
        new_species = save_record(Species, data)
        return jsonify({"message": "Espécie salva com sucesso!", "id": new_species.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Rota para deletar uma espécie pelo ID
@species_bp.route('/especies/<int:id>', methods=['DELETE'])
def delete_species(id):
    s = Species.query.get(id)
    if not s:
        abort(404, description="Espécie não encontrada")

    db.session.delete(s)
    db.session.commit()
    return jsonify({"message": "Espécie deletada com sucesso!"})
