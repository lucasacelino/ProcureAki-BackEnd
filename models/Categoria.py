from helpers.database import db

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_categoria = db.Column(db.String(100), nullable=False)