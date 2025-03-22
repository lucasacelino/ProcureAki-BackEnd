from helpers.database import db

from flask_restful import fields

categoria_fields = {
    'id': fields.Integer,
    'nome_categoria': fields.String
}

class Categoria(db.Model):
    __tablename__ = "tb_categorias"
    
    id = db.Column(db.Integer, primary_key=True)
    nome_categoria = db.Column(db.String(100), nullable=False)
    lojas = db.relationship('Loja', backref='categoria', lazy=True)