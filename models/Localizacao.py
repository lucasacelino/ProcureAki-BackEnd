from helpers.database import db

from flask_restful import fields

localizacao_fields = {
    'id': fields.Integer,
    'latitude': fields.String,
    'longitude': fields.String
}

class Localizacao(db.Model):
    __tablename__ = 'tb_localizacoes'
    
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.String(300), nullable=False)
    longitude = db.Column(db.String(300), nullable=False)