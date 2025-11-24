@login_manager.user_loader
def load_user(user_id):
    user_model = UserModel.query.get(int(user_id))
    
    if not user_model:
        return None
        
    return user_model.to_entity()