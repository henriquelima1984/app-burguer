# Configurando a string de conexão com o MongoDB Atlas
from pymongo import MongoClient

MONGO_URI = ("mongodb+srv://AdminHenrique:EXnkE9RjYDDR57Lx@duettburguer.ni6u7.mongodb.net/?retryWrites=true&w="
             "majority&appName=DuettBurguer")
client = MongoClient(MONGO_URI)

# Escolhendo o bando de dados e coleção
db = client['duett_burguer']
users = db['users']