from helpers.database import db
from flask_restful import fields

produto_fields = {
    'id': fields.Integer,
    'nome': fields.String,
    'preco': fields.Float,
    'quantidade': fields.Integer,
    'imagem_url': fields.String,
    'descricao': fields.String,
    'loja_id': fields.Integer
}

class Produto(db.Model):
    __tablename__ = "tb_produtos"
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Integer, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    imagem_url = db.Column(db.String(100), nullable=False)
    descricao =  db.Column(db.String(300), nullable=False)
    loja_id = db.Column(db.Integer, db.ForeignKey('tb_lojas.id'), nullable=False)
    loja = db.relationship("Loja", back_populates="produtos")
