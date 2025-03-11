from helpers.database import db
from flask_restful import fields

endereco_fields = {
    'id': fields.Integer,
    'cep': fields.String,
    'logradouro': fields.String,
    'bairro': fields.String,
    'cidade': fields.String,
    'estado': fields.String,
    'numero': fields.String,
}

class Endereco(db.Model):
    __tablename__ = "tb_endereco_loja"

    id = db.Column(db.Integer, primary_key=True)
    cep = db.Column(db.String(10), nullable=False)
    logradouro = db.Column(db.String(100), nullable=False)
    bairro = db.Column(db.String(50), nullable=False)
    cidade = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.String(50), nullable=False)
    numero = db.Column(db.Integer, nullable=False)
