from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for, flash, session
from crud import criar_usuario, listar_usuarios, deletar_usuario, atualizar_usuario
from flask_bcrypt import Bcrypt
from database import db

app = Flask(__name__)
app.secret_key = b'p[\xf0\xea\xe2{\xca\xfd\x8c\xf5\x8c\xea\x17\xc5\xd5N\xbb\x8bw\xac0r{\x16'
bcrypt = Bcrypt(app)

def is_admin(email):
    return email.endswith('@duettburguer.com')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        # Verificar se o usuário existe no banco de dados
        user = db.users.find_one({'email': email})

        if user and bcrypt.check_password_hash(user['senha'], senha):
            # Armazenar o ID do usuário ou outro identificador na sessão
            session['user_id'] = str(user['_id'])  # ou qualquer identificador único
            session['role'] = user['role']  # Armazenar a role do usuário

            flash('Login bem-sucedido!', 'success')

            # Redirecionar com base no papel do usuário
            if user['role'] == 'admin':
                return redirect(url_for('admin_panel'))
            else:
                return redirect(url_for('cardapio'))
        else:
            flash('Email ou senha inválidos', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar_usuario():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        if criar_usuario(nome, email, senha):
            return redirect(url_for('login'))

    return render_template('cadastrar.html')

@app.route('/admin/criar_usuario', methods=['GET', 'POST'])
def criar_usuario_admin():
    # Verifica se o usuário logado é administrador
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Acesso não autorizado!', 'danger')
        return redirect(url_for('home'))

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        role = request.form['role']  # Pode ser "admin" ou "cliente"

        # Hash da senha com bcrypt
        hashed_senha = bcrypt.generate_password_hash(senha).decode('utf-8')

        # Verifica duplicidade de email
        if db.users.find_one({"email": email}):
            flash("E-mail já cadastrado!", "error")
            return redirect(url_for('criar_usuario_admin'))

        # Salva o novo usuário no banco de dados
        db.users.insert_one({
            "nome": nome,
            "email": email,
            "senha": hashed_senha,
            "role": role
        })

        flash("Usuário criado com sucesso!", "success")
        return redirect(url_for('admin_panel'))

    return render_template('criar_usuario_admin.html')


# Rota do painel administrativo (apenas para administradores)
@app.route('/admin')
def admin_panel():
    # Verificar se o usuário está logado e se tem a role de admin
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Acesso não autorizado!', 'danger')
        return redirect(url_for('home'))

    usuarios = listar_usuarios() # Listar usuários cadastrados
    return render_template('admin.html', users=usuarios)  # Página do painel do administrador

@app.route('/admin/editar_usuario/<user_id>', methods=['GET', 'POST'])
def editar_usuario(user_id):
    user = db.users.find_one({"_id": ObjectId(user_id)})

    if not user:
        flash('Usuário não encontrado.', 'danger')
        return redirect(url_for('admin_panel'))

    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        role = request.form.get('role')

        # Atualiza os dados no banco de dados
        db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"nome": nome, "email": email, "role": role}}
        )
        flash('Usuário atualizado com sucesso.', 'success')
        return redirect(url_for('admin_panel'))

    return render_template('editar_usuario.html', usuario=user)

@app.route('/admin/deletar_usuario/<user_id>', methods=['POST'])
def deletar_usuario(user_id):
    try:
        result = db.users.delete_one({"_id": ObjectId(user_id)})
        if result.deleted_count == 1:
            flash('Usuário deletado com sucesso.', 'success')
        else:
            flash('Usuário não encontrado.', 'danger')
    except Exception as e:
        flash(f'Erro ao deletar usuário: {str(e)}', 'danger')
    return redirect(url_for('admin_panel'))

@app.route('/logout')
def logout():
    # Limpar a sessão para deslogar
    session.clear()
    flash('Você foi deslogado com sucesso!', 'info')
    return redirect(url_for('home'))

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/cardapio')
def cardapio():
    return render_template('cardapio.html')

@app.route('/contato')
def contato():
    return render_template('contato.html')

if __name__ == '__main__':
    app.run(debug=True)
