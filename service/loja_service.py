from flask import Blueprint, request, jsonify
from flask_restful import marshal_with

from helpers.database import db

from models.Loja import Loja, loja_fields
from models.Endereco import Endereco


loja_bp = Blueprint("lojas", __name__)

@loja_bp.post("/")
def criar_loja():
    data = request.json
    endereco_data = data.get("endereco")

    endereco = Endereco(
        cep = endereco_data["cep"],
        logradouro = endereco_data["logradouro"],
        cidade = endereco_data["cidade"],
        estado = endereco_data["estado"],
        numero = endereco_data["numero"]
    )

    db.session.add(endereco)
    db.session.commit()

    nova_loja = Loja(
        nome = data["nome"],
        descricao = data["descricao"],
        horario_funcionamento = data["horario_funcionamento"],
        telefone = data["telefone"],
        email = data["email"],
        senha = data["senha"],
        endereco_id = endereco.id
    )

    db.session.add(nova_loja)
    db.session.commit()

    return jsonify({"message": "Loja cadastrada com sucesso!"}), 201


@loja_bp.get("/")
@marshal_with(loja_fields)
def getLojaPorId():
    lojas = Loja.query.all()
    return lojas


@loja_bp.put("/<int:loja_id>")
@marshal_with(loja_fields)
def atualizarDadosLoja(loja_id):
    loja = Loja.query.get(loja_id)
    if not loja:
        return {"mensagem": "Loja não encontrada"}, 404

    dados = request.json
    loja.nome = dados.get("nome", loja.nome)
    loja.descricao = dados.get("descricao", loja.descricao)
    loja.horario_funcionamento = dados.get("horario_funcionamento", loja.horario_funcionamento)
    loja.telefone = dados.get("telefone", loja.telefone)
    loja.email = dados.get("email", loja.email)

    db.session.commit()
    return loja, 200


@loja_bp.delete('/<int:loja_id>')
def deletar_loja(loja_id):
    loja = Loja.query.get(loja_id)
    if not loja:
        return {"mensagem": "Loja não encontrada"}, 404

    db.session.delete(loja)
    db.session.commit()
    return {"mensagem": "Loja deletada com sucesso"}, 200
