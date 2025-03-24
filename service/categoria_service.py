from flask import Blueprint
from flask_restful import marshal_with

from models.Categoria import categoria_fields, Categoria

categorias_bp = Blueprint("categorias", __name__)

@categorias_bp.get("")
@marshal_with(categoria_fields)
def getCategorias():
    categorias = Categoria.query.all()
    return categorias, 200
