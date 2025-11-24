from flask import request, jsonify
from flask_login import login_user
from src.infra.db.models.user_model import UserModel

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    
    user_model = UserModel.query.filter_by(email=data.get('email')).first()

    if not user_model:
         return jsonify({"msg": "User not found"}), 401
    
    user_entity = user_model.to_entity()

    if user_entity.password == data.get('password'):
        login_user(user_entity) 
        return jsonify({"message": "Logado com sucesso!"})
    
    return jsonify({"message": "Senha errada"}), 401