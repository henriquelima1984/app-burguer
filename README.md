# Duett Burger - Sistema de Gerenciamento e Cardápio

Este é um projeto básico desenvolvido em Flask para gerenciar e consumir os serviços da hamburgueria Duett Burger. Ele inclui funcionalidades de autenticação, painel administrativo, CRUD de usuários, e navegação para clientes.

---

## Pré-requisitos

Antes de começar, certifique-se de ter o seguinte:

- **Python** (versão 3.8 ou superior)
- Gerenciador de pacotes **pip**
- Uma conta no [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) configurada com um cluster e banco de dados.

---

## Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio

2. ## Crie e ative um ambiente virtual:<br>
  python -m venv venv<br>
  source venv/bin/activate  # Linux/MacOS<br>
  venv\Scripts\activate     # Windows<br>

3. ## Instale as dependências:<br>
  pip install -r requirements.txt<br>
  
4. ## Configuração do MongoDB Atlas:<br>
  mongodb+srv://<usuario>:<senha>@cluster0.mongodb.net/<seu-database>?retryWrites=true&w=majority
  Substitua <usuario>, <senha> e <seu-database> pelas credenciais e nome do banco configurados.<br>

5. ## Configure variáveis de ambiente
   MONGO_URI=mongodb+srv://<usuario>:<senha>@cluster0.mongodb.net/<seu-database>?retryWrites=true&w=majority
app.secret_key=sua_chave_secreta_aqui
(Recomenda-se que seja criado um arquivo .env para armazenar essas informações, mas aqui por questões de estudo criei um arquivo database.py para mostrar como conectar com o banco).<br>

6. ## Rode a aplicação:
   flask run
