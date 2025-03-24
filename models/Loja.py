from helpers.database import db
from flask_restful import fields
from flask import jsonify

from models.Endereco import endereco_fields
from models.Categoria import categoria_fields
from models.Localizacao import localizacao_fields

from datetime import datetime
# from marshmallow import fields, Field
from marshmallow.fields import Field

class TimeField(Field):
    def _serialize(self, value):
        if value is None:
            return None
        return value.strftime('%H:%M')

    def _deserialize(self, value):
        try:
            return datetime.strptime(value, '%H:%M').time()
        except ValueError as error:
            return jsonify({'error': str(error)})

loja_fields = {
    'id': fields.Integer,
    'nome': fields.String,
    'cnpj': fields.String,
    'senha': fields.String,
    'descricao': fields.String,
    'horario_inicio': TimeField(),  
    'horario_fim': TimeField(),
    'telefone': fields.String,
    'email': fields.String,
    'endereco': fields.Nested(endereco_fields),
    'categoria': fields.Nested(categoria_fields),
    'localizacao': fields.Nested(localizacao_fields)
}

class Loja(db.Model):
    __tablename__ = "tb_lojas"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(20), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    # horario_funcionamento = db.Column(db.String(50), nullable=False)
    # horario_inicio = db.Column(db.String(50), nullable=False)  # Novo campo
    # horario_fim = db.Column(db.String(50), nullable=False)
    horario_inicio = db.Column(db.Time, nullable=False)  # Alterado para time
    horario_fim = db.Column(db.Time, nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('tb_categorias.id'), nullable=False)
    endereco_id = db.Column(db.Integer, db.ForeignKey("tb_endereco_loja.id"), nullable=False)
    localizacao_id = db.Column(db.Integer, db.ForeignKey("tb_localizacoes.id"), unique=True, nullable=False)
    localizacao = db.relationship("Localizacao", backref=db.backref("loja", uselist=False))
    endereco = db.relationship("Endereco", backref=db.backref("loja", uselist=False))
    produtos = db.relationship("Produto", back_populates="loja", cascade="all, delete-orphan")
