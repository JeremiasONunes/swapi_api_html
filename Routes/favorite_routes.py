# -----------------------------------------------------------------------------
# Versão em Português:
# Este código implementa um serviço web para gerenciar favoritos relacionados à
# franquia Star Wars. Ele permite listar, adicionar, deletar e buscar favoritos 
# no banco de dados local, utilizando o Flask como framework web e SQLAlchemy 
# para manipulação do banco de dados.
#
# English Version:
# This code implements a web service for managing favorites related to the Star 
# Wars franchise. It allows listing, adding, deleting, and fetching favorites 
# from the local database using Flask as the web framework and SQLAlchemy for 
# database handling.
#
# Copyright © 2024 Jeremias Nunes. All rights reserved.
# Copyright © 2024 Rafael Mesquita. All rights reserved.
# -----------------------------------------------------------------------------

from flask import Blueprint, jsonify, request
from models import db, Favorite

# Criação do Blueprint para a rota de favoritos
favorite_bp = Blueprint('favorite', __name__)

# Função auxiliar para salvar um novo registro no banco de dados
def save_record(model, data):
    new_record = model(**data)
    db.session.add(new_record)
    db.session.commit()
    return new_record

# Rota para salvar um favorito no banco de dados
@favorite_bp.route('/favorito/save', methods=['POST'])
def save_favorite():
    data = request.json
    required_fields = ["character_id", "student_name1", "registration1"]

    # Verificação de campos obrigatórios
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Campos obrigatórios ausentes"}), 400

    # Adiciona campos opcionais ao dicionário de dados
    optional_fields = [
        "movie_id", "starship_id", "vehicle_id", "species_id",
        "planet_id", "student_name2", "registration2", "course",
        "university", "period"
    ]
    
    # Mantém valores ou define como None
    for field in optional_fields:
        data[field] = data.get(field, None)

    # Salva o novo favorito
    new_favorite = save_record(Favorite, data)
    return jsonify({"message": "Favorito salvo com sucesso!", "id": new_favorite.id}), 201

# Rota para listar todos os favoritos salvos
@favorite_bp.route('/favorito', methods=['GET'])
def list_favorites():
    favorites = Favorite.query.all()
    result = []

    # Cria uma lista de favoritos para retornar
    for f in favorites:
        result.append({
            "id": f.id,
            "character_id": f.character_id,
            "movie_id": f.movie_id,
            "starship_id": f.starship_id,
            "vehicle_id": f.vehicle_id,
            "species_id": f.species_id,
            "planet_id": f.planet_id,
            "student_name1": f.student_name1,
            "registration1": f.registration1,
            "student_name2": f.student_name2,
            "registration2": f.registration2,
            "course": f.course,
            "university": f.university,
            "period": f.period
        })

    return jsonify(result)

# Rota para buscar um favorito específico pelo ID
@favorite_bp.route('/favorito/<int:id>', methods=['GET'])
def get_favorite(id):
    f = Favorite.query.get(id)

    # Verifica se o favorito foi encontrado
    if not f:
        return jsonify({"error": "Favorito não encontrado"}), 404

    # Retorna os dados do favorito
    result = {
        "character_id": f.character_id,
        "movie_id": f.movie_id,
        "starship_id": f.starship_id,
        "vehicle_id": f.vehicle_id,
        "species_id": f.species_id,
        "planet_id": f.planet_id,
        "student_name1": f.student_name1,
        "registration1": f.registration1,
        "student_name2": f.student_name2,
        "registration2": f.registration2,
        "course": f.course,
        "university": f.university,
        "period": f.period
    }
    return jsonify(result)

# Rota para deletar um favorito pelo ID
@favorite_bp.route('/favorito/delete/<int:id>', methods=['DELETE'])
def delete_favorite(id):
    f = Favorite.query.get(id)

    # Verifica se o favorito foi encontrado
    if f:
        db.session.delete(f)
        db.session.commit()
        return jsonify({"message": "Favorito deletado com sucesso!"})
    
    return jsonify({"error": "Favorito não encontrado"}), 404
