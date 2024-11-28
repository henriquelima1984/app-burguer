from flask import flash
from flask_bcrypt import Bcrypt
from database import db

bcrypt = Bcrypt()

def criar_usuario(nome,email,senha):
    hashed_senha = bcrypt.generate_password_hash(senha).decode('utf-8')
    role = 'admin' if email.endswith('@duettburguer.com') else 'cliente'

    # Verifica se o email já está cadastrado
    if db.users.find_one({"email": email}):
        flash("E-mail já cadastrado!", "error")
        return False

    # Salva o usuário no banco de dados
    db.users.insert_one({
        "nome": nome,
        "email": email,
        "senha": hashed_senha,
        "role": role
    })

    flash("Cadastrado realizado com sucesso!", "success")
    return True

# Função para listar todos os usuários
def listar_usuarios():
    return db.users.find()

# Função para deletar um usuário
def deletar_usuario(user_id):
    db.users.delete_one({"_id": user_id})
    flash("Usuário deletado com sucesso!", "success")

# Função para atualizar dados de um usuário
def atualizar_usuario(user_id, nome, email, senha):
    hashed_senha = bcrypt.generate_password_hash(senha).decode('utf-8')

    db.users.update_one(
        {"_id": user_id},
        {"$set": {
            "nome": nome,
            "email": email,
            "senha": hashed_senha
        }}
    )
    flash("Dados atualizados com sucesso!", "success")
