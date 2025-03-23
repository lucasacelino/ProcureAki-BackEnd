from flask import Blueprint, request, jsonify
from flask_restful import marshal_with, reqparse, marshal

from helpers.database import db
from models.Loja import Loja, loja_fields
from models.Endereco import Endereco
from models.Categoria import Categoria
from models.Localizacao import Localizacao

loja_bp = Blueprint("lojas", __name__)

parser = reqparse.RequestParser()
parser.add_argument('nome', type=str, required=True, help="O campo 'nome' é obrigatório.")
parser.add_argument('cnpj', type=str, required=True, help="O campo 'nome' é obrigatório.")
parser.add_argument('descricao', type=str, required=True, help="O campo 'preço' deve ser um número válido.")
parser.add_argument('horario_funcionamento', type=str, required=True, help="O campo 'quantidade' deve ser um número inteiro.")
parser.add_argument('telefone', type=str, required=True, help="O campo 'imagem' é obrigatório.")
parser.add_argument('email', type=str, required=True, help="O campo 'descricao' é obrigatório.")
parser.add_argument('senha', type=str, required=True, help="O campo 'senha' é obrigatório.")
parser.add_argument('endereco', type=dict, required=True, help="O campo 'loja_id' é obrigatório e deve ser um número inteiro.")
parser.add_argument('categoria', type=dict, required=True, help="O campo categoria é obrigatório")
parser.add_argument('localizacao', type=dict, required=True, help="o campo localização é obrigatório")


@loja_bp.post("")
def criar_loja():
    try:
        dados = parser.parse_args()
        endereco_data = dados.get("endereco")
        if not endereco_data:
            return jsonify({'messagem': 'É obrigatório passar os dados do endereço'})
        endereco = Endereco(
            cep = endereco_data["cep"],
            logradouro = endereco_data["logradouro"],
            bairro = endereco_data["bairro"],
            cidade = endereco_data["cidade"],
            estado = endereco_data["estado"],
            numero = endereco_data["numero"]
        )
        db.session.add(endereco)
        db.session.commit()
        
        
        categoria_data = dados.get("categoria")
        if not categoria_data:
            return jsonify({'mensagem': 'É obrigatório informar a categoria'})
        categoria = Categoria(
            nome_categoria = categoria_data["nome_categoria"]
        )
        db.session.add(categoria)
        db.session.commit()


        localizacao_data = dados.get("localizacao")
        if not localizacao_data:
            return jsonify({'mensagem': 'É obrigatório informar a localização'})
        localizacao = Localizacao(
            latitude = localizacao_data["latitude"],
            longitude = localizacao_data["longitude"]
        )
        db.session.add(localizacao)
        db.session.commit()
        
        
        nova_loja = Loja(
            nome = dados["nome"],
            cnpj = dados["cnpj"],
            descricao = dados["descricao"],
            horario_funcionamento = dados["horario_funcionamento"],
            telefone = dados["telefone"],
            email = dados["email"],
            senha = dados["senha"],
            categoria_id = categoria.id,
            endereco_id = endereco.id,
            localizacao_id = localizacao.id
        )

        db.session.add(nova_loja)
        db.session.commit()

        return jsonify({"message": "Loja cadastrada com sucesso!"}), 201
    
    except Exception as e:
        return jsonify({'erro': f'Erro ao criar Loja: {str(e)}'}), 500


@loja_bp.get("/")
@marshal_with(loja_fields)
def getLojas():
    lojas = Loja.query.all()
    return lojas


@loja_bp.get("/<string:nomeCategoria>")
@marshal_with(loja_fields)
def getLojasPorCategoria(nomeCategoria):
    if not nomeCategoria:
        return jsonify({"mensagem": "O nome da categoria é obrigatório."}), 400

    lojas = Loja.query.join(Categoria).filter(Categoria.nome_categoria == nomeCategoria).all()

    if not lojas:
        return jsonify({"mensagem": f"Nenhuma loja encontrada para a categoria '{nomeCategoria}'."}), 404

    return lojas


@loja_bp.put("/<int:loja_id>")
@marshal_with(loja_fields)
def atualizarDadosLoja(loja_id):
    try:
        loja = Loja.query.get(loja_id)
        if not loja:
            return {"mensagem": "Loja não encontrada"}, 404

        dados = request.json
        loja.nome = dados.get("nome", loja.nome)
        loja.descricao = dados.get("descricao", loja.descricao)
        loja.senha = dados.get("senha", loja.senha)
        loja.horario_funcionamento = dados.get("horario_funcionamento", loja.horario_funcionamento)
        loja.telefone = dados.get("telefone", loja.telefone)
        loja.email = dados.get("email", loja.email)

        db.session.commit()
        return loja, 200
    
    except Exception as e:
        return jsonify({'erro': f'Erro ao atualizar loja: {str(e)}'}), 500


@loja_bp.delete('/<int:loja_id>')
def deletar_loja(loja_id):
    try:
        loja = Loja.query.get(loja_id)
        if not loja:
            return {"mensagem": "Loja não encontrada"}, 404

        db.session.delete(loja)
        db.session.commit()
        return {"mensagem": "Loja deletada com sucesso"}, 200
    
    except Exception as e:
        return jsonify({'erro': f'Erro ao deletar loja: {str(e)}'}), 500
