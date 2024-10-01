# -----------------------------------------------------------------------------
# Versão em Português:
# Este código implementa um serviço web para gerenciar veículos da franquia 
# Star Wars. Ele permite listar, adicionar, excluir e buscar veículos na base 
# de dados local, bem como buscar veículos diretamente da API SWAPI. Utiliza 
# Flask como framework web e SQLAlchemy para manipulação do banco de dados.

# English Version:
# This code implements a web service for managing vehicles from the Star Wars 
# franchise. It allows listing, adding, deleting, and fetching vehicles from 
# the local database, as well as retrieving vehicles directly from the SWAPI API. 
# Flask is used as the web framework, and SQLAlchemy is used for database handling.

# Copyright © 2024 Jeremias Nunes. All rights reserved.
# Copyright © 2024 Rafael Mesquita. All rights reserved.
# -----------------------------------------------------------------------------
from flask import Blueprint, jsonify, request, abort
import requests
import json
from datetime import datetime

from models import db, Vehicle

# Criação do Blueprint
vehicle_bp = Blueprint('vehicles', __name__)

# Função auxiliar para salvar um novo registro
def save_record(model, data):
    if not all(key in data for key in ('name', 'model')):  # Verificação de campos
        raise ValueError("Dados insuficientes para criar um registro.")
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

# Função para buscar veículos da SWAPI e salvar no banco de dados
def fetch_and_save_vehicles():
    swapi_data = fetch_from_swapi('vehicles')
    if swapi_data:
        for item in swapi_data['results']:
            vehicle_data = {
                "name": item["name"],
                "model": item["model"],
                "manufacturer": item.get("manufacturer"),
                "cost_in_credits": item.get("cost_in_credits"),
                "length": item.get("length"),
                "max_atmosphering_speed": item.get("max_atmosphering_speed"),
                "crew": item.get("crew"),
                "passengers": item.get("passengers"),
                "cargo_capacity": item.get("cargo_capacity"),
                "consumables": item.get("consumables"),
                "vehicle_class": item.get("vehicle_class"),
            }
            try:
                # Evitar duplicatas: verifica se o veículo já está salvo
                if not Vehicle.query.filter_by(name=vehicle_data['name'], model=vehicle_data['model']).first():
                    save_record(Vehicle, vehicle_data)
            except Exception as e:
                print(f"Falha ao salvar veículo {item['name']}: {str(e)}")

# Rota para listar todos os veículos (e buscar da SWAPI se o banco de dados estiver vazio)
@vehicle_bp.route('/veiculos', methods=['GET'])
def get_vehicles():
    # Verifica se há veículos no banco de dados local, caso contrário busca da SWAPI
    if not Vehicle.query.first():
        fetch_and_save_vehicles()
    
    # Agora busca todos os veículos do banco de dados
    vehicles_list = Vehicle.query.all()
    result = [{
        "id": v.id,
        "name": v.name,
        "model": v.model,
        "manufacturer": v.manufacturer,
        "cost_in_credits": v.cost_in_credits,
        "length": v.length,
        "max_atmosphering_speed": v.max_atmosphering_speed,
        "crew": v.crew,
        "passengers": v.passengers,
        "cargo_capacity": v.cargo_capacity,
        "consumables": v.consumables,
        "vehicle_class": v.vehicle_class,
        "created": v.created.isoformat(),
        "edited": v.edited.isoformat(),
    } for v in vehicles_list]
    
    return jsonify(result)

# Rota para retornar um veículo específico pelo ID
@vehicle_bp.route('/veiculos/<int:id>', methods=['GET'])
def get_vehicle_by_id(id):
    v = Vehicle.query.get(id)
    if not v:
        abort(404, description="Veículo não encontrado")
    
    return jsonify({
        "id": v.id,
        "name": v.name,
        "model": v.model,
        "manufacturer": v.manufacturer,
        "cost_in_credits": v.cost_in_credits,
        "length": v.length,
        "max_atmosphering_speed": v.max_atmosphering_speed,
        "crew": v.crew,
        "passengers": v.passengers,
        "cargo_capacity": v.cargo_capacity,
        "consumables": v.consumables,
        "vehicle_class": v.vehicle_class,
        "created": v.created.isoformat(),
        "edited": v.edited.isoformat(),
    })

# Rota para salvar um novo veículo no banco de dados
@vehicle_bp.route('/veiculos', methods=['POST'])
def save_vehicle():
    data = request.json
    if not data or 'name' not in data:  # Verificação de dados
        return jsonify({"error": "Dados inválidos!"}), 400
    try:
        new_vehicle = save_record(Vehicle, data)
        return jsonify({"message": "Veículo salvo com sucesso!", "id": new_vehicle.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Rota para deletar um veículo pelo ID
@vehicle_bp.route('/veiculos/<int:id>', methods=['DELETE'])
def delete_vehicle(id):
    v = Vehicle.query.get(id)
    if not v:
        abort(404, description="Veículo não encontrado")
    
    db.session.delete(v)
    db.session.commit()
    return jsonify({"message": "Veículo deletado com sucesso!"})
