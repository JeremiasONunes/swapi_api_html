# -----------------------------------------------------------------------------
# Versão em Português:
# Este código implementa um serviço web para gerenciar naves da franquia Star Wars. 
# Ele permite listar, adicionar, excluir e buscar naves na base de dados local, 
# bem como buscar naves diretamente da API SWAPI. Utiliza Flask como framework web 
# e SQLAlchemy para manipulação do banco de dados.
# 
# English Version:
# This code implements a web service for managing starships from the Star Wars 
# franchise. It allows listing, adding, deleting, and fetching starships from 
# the local database, as well as retrieving starships directly from the SWAPI API. 
# Flask is used as the web framework, and SQLAlchemy is used for database handling.
#
# Copyright © 2024 Jeremias Nunes. All rights reserved.
# Copyright © 2024 Rafael Mesquita. All rights reserved.
# -----------------------------------------------------------------------------

from flask import Blueprint, jsonify, request, abort
from models import db, Starship
import requests
import json

# Criação do Blueprint
starship_bp = Blueprint('starships', __name__)

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

# Função auxiliar para converter valores
def convert_value(value):
    if isinstance(value, str):
        value = value.replace(',', '')  # Remove vírgulas
        if value.isdigit():
            return int(value)  # Converte para inteiro
        try:
            return float(value)  # Converte para float
        except ValueError:
            return value  # Retorna o valor original se não puder converter
    return value

# Função para buscar naves da SWAPI e salvar no banco de dados
def fetch_and_save_starships():
    next_url = 'starships'
    while next_url:
        swapi_data = fetch_from_swapi(next_url)
        if swapi_data:
            for item in swapi_data['results']:
                starship_data = {
                    "name": item["name"],
                    "model": item["model"],
                    "manufacturer": item["manufacturer"],
                    "cost_in_credits": convert_value(item.get("cost_in_credits")),
                    "length": convert_value(item.get("length")),
                    "max_atmosphering_speed": convert_value(item.get("max_atmosphering_speed")),
                    "crew": convert_value(item.get("crew")),
                    "passengers": convert_value(item.get("passengers")),
                    "cargo_capacity": convert_value(item.get("cargo_capacity")),
                    "consumables": item.get("consumables"),
                    "hyperdrive_rating": convert_value(item.get("hyperdrive_rating")),
                    "MGLT": convert_value(item.get("MGLT")),
                    "starship_class": item.get("starship_class"),
                }
                try:
                    # Evitar duplicatas: verifica se a nave já está salva
                    if not Starship.query.filter_by(name=starship_data['name']).first():
                        save_record(Starship, starship_data)
                        print(f"Nave {starship_data['name']} salva com sucesso.")
                    else:
                        print(f"Nave {starship_data['name']} já existe no banco de dados.")
                except Exception as e:
                    print(f"Falha ao salvar nave {item['name']}: {str(e)}")
            next_url = swapi_data.get('next')  # Verifica se há uma próxima página
        else:
            break

# Rota para listar todas as naves (e buscar da SWAPI se o banco de dados estiver vazio)
@starship_bp.route('/naves', methods=['GET'])
def get_naves():
    # Verifica se há naves no banco de dados local, caso contrário busca da SWAPI
    if not Starship.query.first():
        fetch_and_save_starships()
    
    # Agora busca todas as naves do banco de dados
    naves_list = Starship.query.all()
    result = [{
        "id": n.id,
        "name": n.name,
        "model": n.model,
        "manufacturer": n.manufacturer,
        "cost_in_credits": n.cost_in_credits,
        "length": n.length,
        "max_atmosphering_speed": n.max_atmosphering_speed,
        "crew": n.crew,
        "passengers": n.passengers,
        "cargo_capacity": n.cargo_capacity,
        "consumables": n.consumables,
        "hyperdrive_rating": n.hyperdrive_rating,
        "MGLT": n.MGLT,
        "starship_class": n.starship_class
    } for n in naves_list]
    
    return jsonify(result)

# Rota para retornar uma nave específica pelo ID
@starship_bp.route('/naves/<int:id>', methods=['GET'])
def get_nave(id):
    n = Starship.query.get(id)
    if not n:
        abort(404, description="Nave não encontrada")
    
    return jsonify({
        "id": n.id,
        "name": n.name,
        "model": n.model,
        "manufacturer": n.manufacturer,
        "cost_in_credits": n.cost_in_credits,
        "length": n.length,
        "max_atmosphering_speed": n.max_atmosphering_speed,
        "crew": n.crew,
        "passengers": n.passengers,
        "cargo_capacity": n.cargo_capacity,
        "consumables": n.consumables,
        "hyperdrive_rating": n.hyperdrive_rating,
        "MGLT": n.MGLT,
        "starship_class": n.starship_class
    })

# Rota para salvar uma nave no banco de dados
@starship_bp.route('/naves', methods=['POST'])
def save_nave():
    data = request.json
    try:
        new_nave = save_record(Starship, data)
        return jsonify({"message": "Nave salva com sucesso!", "id": new_nave.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Rota para deletar uma nave pelo ID
@starship_bp.route('/naves/<int:id>', methods=['DELETE'])
def delete_nave(id):
    n = Starship.query.get(id)
    if not n:
        abort(404, description="Nave não encontrada")
    
    db.session.delete(n)
    db.session.commit()
    return jsonify({"message": "Nave deletada com sucesso!"})
