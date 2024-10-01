# -----------------------------------------------------------------------------
# Versão em Português:
# Este código implementa um serviço web para gerenciar personagens da franquia 
# Star Wars. Ele permite listar, adicionar, excluir e buscar personagens na base 
# de dados local, bem como buscar personagens diretamente da API SWAPI. Utiliza 
# Flask como framework web e SQLAlchemy para manipulação do banco de dados.

# English Version:
# This code implements a web service for managing characters from the Star Wars 
# franchise. It allows listing, adding, deleting, and fetching characters from 
# the local database, as well as retrieving characters directly from the SWAPI API. 
# Flask is used as the web framework, and SQLAlchemy is used for database handling.

# Copyright © 2024 Jeremias Nunes. All rights reserved.
# Copyright © 2024 Rafael Mesquita. All rights reserved.
# -----------------------------------------------------------------------------
from flask import Blueprint, jsonify, request, abort 
import requests  

from models import db, Character

import json

# Criação do Blueprint
character_bp = Blueprint('characters', __name__)

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
        response.raise_for_status()  # Verifica erros na resposta
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching from SWAPI: {e}")
        return None

# Função para buscar personagens da SWAPI e salvar no banco de dados
def fetch_and_save_characters():
    swapi_data = fetch_from_swapi('people')
    if swapi_data:
        for item in swapi_data['results']:
            character_data = {
                "name": item["name"],
                "height": item["height"],
                "mass": item["mass"],
                "hair_color": item.get("hair_color"),
                "skin_color": item.get("skin_color"),
                "eye_color": item.get("eye_color"),
                "birth_year": item.get("birth_year"),
                "gender": item.get("gender"),
                "homeworld": item.get("homeworld"),
                "films": json.dumps(item.get("films", [])),  # Armazenar como JSON
                "species": json.dumps(item.get("species", [])),  # Armazenar como JSON
                "vehicles": json.dumps(item.get("vehicles", [])),  # Armazenar como JSON
                "starships": json.dumps(item.get("starships", [])),  # Armazenar como JSON
            }
            try:
                # Evitar duplicatas: verifica se o personagem já está salvo
                if not Character.query.filter_by(name=character_data['name']).first():
                    save_record(Character, character_data)
            except Exception as e:
                print(f"Falha ao salvar personagem {item['name']}: {str(e)}")

# Rota para listar todos os personagens (e buscar da SWAPI se o banco de dados estiver vazio)
@character_bp.route('/personagens', methods=['GET'])
def get_personagens():
    # Verifica se há personagens no banco de dados local, caso contrário busca da SWAPI
    if not Character.query.first():
        fetch_and_save_characters()
    
    # Agora busca todos os personagens do banco de dados
    personagens_list = Character.query.all()
    result = [{
        "id": p.id,
        "name": p.name,
        "height": p.height,
        "mass": p.mass,
        "hair_color": p.hair_color,
        "skin_color": p.skin_color,
        "eye_color": p.eye_color,
        "birth_year": p.birth_year,
        "gender": p.gender,
        "homeworld": p.homeworld,
        "films": load_json(p.films),
        "species": load_json(p.species),
        "vehicles": load_json(p.vehicles),
        "starships": load_json(p.starships),
        "created": p.created.isoformat(),
        "edited": p.edited.isoformat(),
    } for p in personagens_list]
    return render_template('personagens.html', personagens=personagens)
    ##return jsonify(result)

# Rota para retornar um personagem específico pelo ID
@character_bp.route('/personagens/<int:id>', methods=['GET'])
def get_personagem(id):
    p = Character.query.get(id)
    if not p:
        abort(404, description="Personagem não encontrado")
    
    return jsonify({
        "id": p.id,
        "name": p.name,
        "height": p.height,
        "mass": p.mass,
        "hair_color": p.hair_color,
        "skin_color": p.skin_color,
        "eye_color": p.eye_color,
        "birth_year": p.birth_year,
        "gender": p.gender,
        "homeworld": p.homeworld,
        "films": load_json(p.films),
        "species": load_json(p.species),
        "vehicles": load_json(p.vehicles),
        "starships": load_json(p.starships),
        "created": p.created.isoformat(),
        "edited": p.edited.isoformat(),
    })

# Rota para salvar um personagem no banco de dados
@character_bp.route('/personagens', methods=['POST'])
def save_personagem():
    data = request.json
    try:
        # Converte os campos que precisam ser armazenados como JSON
        data['films'] = json.dumps(data.get('films', []))
        data['species'] = json.dumps(data.get('species', []))
        data['vehicles'] = json.dumps(data.get('vehicles', []))
        data['starships'] = json.dumps(data.get('starships', []))
        
        new_personagem = save_record(Character, data)
        return jsonify({"message": "Personagem salvo com sucesso!", "id": new_personagem.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Rota para deletar um personagem pelo ID
@character_bp.route('/personagens/<int:id>', methods=['DELETE'])
def delete_personagem(id):
    p = Character.query.get(id)
    if not p:
        abort(404, description="Personagem não encontrado")
    
    db.session.delete(p)
    db.session.commit()
    return jsonify({"message": "Personagem deletado com sucesso!"})
