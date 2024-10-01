# -----------------------------------------------------------------------------
# Versão em Português:
# Este código implementa um serviço web para gerenciar planetas da franquia 
# Star Wars. Ele permite listar, adicionar, excluir e buscar planetas na base 
# de dados local. Utiliza Flask como framework web e SQLAlchemy para manipulação
# do banco de dados.
#
# English Version:
# This code implements a web service for managing planets from the Star Wars 
# franchise. It allows listing, adding, deleting, and fetching planets from the
# local database. Flask is used as the web framework, and SQLAlchemy is used for
# database handling.
#
# Copyright © 2024 Jeremias Nunes. All rights reserved.
# Copyright © 2024 Rafael Mesquita. All rights reserved.
# -----------------------------------------------------------------------------

from flask import Blueprint, jsonify, request, abort
from models import db, Planet
import json
import requests  # Para futuras requisições à SWAPI (seguindo o mesmo padrão do código de personagens)

# Criação do Blueprint
planet_bp = Blueprint('planets', __name__)

# Função auxiliar para salvar um novo registro
def save_record(model, data):
    try:
        new_record = model(**data)
        db.session.add(new_record)
        db.session.commit()
        return new_record
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Erro ao salvar o registro: {str(e)}")

# Função auxiliar para deserializar JSON
def load_json(value):
    try:
        return json.loads(value) if value else []
    except json.JSONDecodeError:
        return []

# Função auxiliar para buscar dados externos (exemplo da SWAPI)
def fetch_from_swapi(endpoint):
    try:
        response = requests.get(f"https://swapi.dev/api/{endpoint}/")
        response.raise_for_status()  # Verifica erros na resposta
        return response.json()
    except requests.RequestException as e:
        print(f"Erro ao buscar da SWAPI: {e}")
        return None

# Função para buscar planetas da SWAPI e salvar no banco de dados
def fetch_and_save_planets():
    swapi_data = fetch_from_swapi('planets')
    if swapi_data:
        for item in swapi_data['results']:
            planet_data = {
                "name": item["name"],
                "rotation_period": item["rotation_period"],
                "orbital_period": item["orbital_period"],
                "diameter": item["diameter"],
                "climate": item.get("climate"),
                "gravity": item.get("gravity"),
                "terrain": item.get("terrain"),
                "surface_water": item.get("surface_water"),
                "population": item.get("population")
            }
            try:
                # Evitar duplicatas: verifica se o planeta já está salvo
                if not Planet.query.filter_by(name=planet_data['name']).first():
                    save_record(Planet, planet_data)
            except Exception as e:
                print(f"Falha ao salvar planeta {item['name']}: {str(e)}")

# Rota para listar todos os planetas (e buscar da SWAPI se o banco de dados estiver vazio)
@planet_bp.route('/planetas', methods=['GET'])
def get_planetas():
    # Verifica se há planetas no banco de dados local, caso contrário busca da SWAPI
    if not Planet.query.first():
        fetch_and_save_planets()
    
    # Agora busca todos os planetas do banco de dados
    planetas_list = Planet.query.all()
    if not planetas_list:
        abort(404, description="Nenhum planeta encontrado")

    result = [{
        "id": p.id,
        "name": p.name,
        "rotation_period": p.rotation_period,
        "orbital_period": p.orbital_period,
        "diameter": p.diameter,
        "climate": p.climate,
        "gravity": p.gravity,
        "terrain": p.terrain,
        "surface_water": p.surface_water,
        "population": p.population
    } for p in planetas_list]
    
    return jsonify(result)

# Rota para retornar um planeta específico pelo ID
@planet_bp.route('/planetas/<int:id>', methods=['GET'])
def get_planeta(id):
    p = Planet.query.get(id)
    if not p:
        abort(404, description="Planeta não encontrado")
    
    return jsonify({
        "id": p.id,
        "name": p.name,
        "rotation_period": p.rotation_period,
        "orbital_period": p.orbital_period,
        "diameter": p.diameter,
        "climate": p.climate,
        "gravity": p.gravity,
        "terrain": p.terrain,
        "surface_water": p.surface_water,
        "population": p.population
    })

# Rota para salvar um planeta no banco de dados
@planet_bp.route('/planetas', methods=['POST'])
def save_planeta():
    data = request.json
    try:
        new_planeta = save_record(Planet, data)
        return jsonify({"message": "Planeta salvo com sucesso!", "id": new_planeta.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Rota para deletar um planeta pelo ID
@planet_bp.route('/planetas/<int:id>', methods=['DELETE'])
def delete_planeta(id):
    p = Planet.query.get(id)
    if not p:
        abort(404, description="Planeta não encontrado")
    
    try:
        db.session.delete(p)
        db.session.commit()
        return jsonify({"message": "Planeta deletado com sucesso!"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
