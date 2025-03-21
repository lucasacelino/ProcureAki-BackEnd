from helpers.database import db
from flask_restful import fields

from models.Endereco import endereco_fields
from models.Categoria import categoria_fields


loja_fields = {
    'id': fields.Integer,
    'nome': fields.String,
    'descricao': fields.String,
    'horario_funcionamento': fields.String,
    'telefone': fields.String,
    'email': fields.String,
    'endereco': fields.Nested(endereco_fields),
    'categoria': fields.Nested(categoria_fields)
}

class Loja(db.Model):
    __tablename__ = "tb_lojas"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(20), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    horario_funcionamento = db.Column(db.String(50), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('tb_categorias.id'), nullable=False)
    endereco_id = db.Column(db.Integer, db.ForeignKey("tb_endereco_loja.id"), nullable=False)
    endereco = db.relationship("Endereco", backref=db.backref("loja", uselist=False))
    produtos = db.relationship("Produto", back_populates="loja", cascade="all, delete-orphan")

