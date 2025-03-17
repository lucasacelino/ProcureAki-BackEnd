from flask import Blueprint, request, jsonify
from helpers.database import db
from models.Produto import Produto, produto_fields
from flask_restful import marshal_with, reqparse

produto_bp = Blueprint("produtos", __name__)

parser = reqparse.RequestParser()
parser.add_argument('nome', type=str, required=True, help="O campo 'nome' é obrigatório.")
parser.add_argument('preco', type=float, required=True, help="O campo 'preço' deve ser um número válido.")
parser.add_argument('quantidade', type=int, required=True, help="O campo 'quantidade' deve ser um número inteiro.")
parser.add_argument('imagem_url', type=str, required=True, help="O campo 'imagem' é obrigatório.")
parser.add_argument('descricao', type=str, required=True, help="O campo 'descricao' é obrigatório.")
parser.add_argument('loja_id', type=int, required=True, help="O campo 'loja_id' é obrigatório e deve ser um número inteiro.")


@produto_bp.post('/')
@marshal_with(produto_fields)
def criar_produto():
    try:
        dados = parser.parse_args()
        
        novo_produto = Produto(
            nome = dados['nome'],
            preco = dados['preco'],
            quantidade = dados['quantidade'],
            imagem_url = dados['imagem_url'],
            descricao = dados['descricao'],
            loja_id = dados['loja_id']
        )

        db.session.add(novo_produto)
        db.session.commit()
        
        return novo_produto, 201
    except Exception as e:
        return jsonify({'erro': f'Erro ao criar produto: {str(e)}'}), 500


@produto_bp.route('/', methods=['GET'])
@marshal_with(produto_fields)
def listar_produtos():
    try:
        produtos = Produto.query.all()
        return produtos, 200
    except Exception as e:
        return jsonify({'erro': f'Erro ao listar produtos: {str(e)}'}), 500


@produto_bp.route('/produtos/<int:id>', methods=['GET'])
@marshal_with(produto_fields)
def buscar_produto(id):
    try:
        produto = Produto.query.get(id)
        if not produto:
            return jsonify({'erro': 'Produto não encontrado'}), 404
        return produto, 200
    except Exception as e:
        return jsonify({'erro': f'Erro ao buscar produto: {str(e)}'}), 500


@produto_bp.route('/produtos/<int:id>', methods=['PUT'])
@marshal_with(produto_fields)
def atualizar_produto(id):
    try:
        produto = Produto.query.get(id)
        if not produto:
            return jsonify({'erro': 'Produto não encontrado'}), 404

        dados = parser.parse_args()

        produto.nome = dados.get('nome', produto.nome)
        produto.preco = dados.get('preco', produto.preco)
        produto.quantidade = dados.get('quantidade', produto.quantidade)
        produto.imagem_url = dados.get('imagem_url', produto.imagem_url)
        produto.descricao = dados.get('descricao', produto.descricao)

        db.session.commit()
        return produto, 200
    except Exception as e:
        return jsonify({'erro': f'Erro ao atualizar produto: {str(e)}'}), 500


@produto_bp.route('/produtos/<int:id>', methods=['DELETE'])
def deletar_produto(id):
    try:
        produto = Produto.query.get(id)
        if not produto:
            return jsonify({'erro': 'Produto não encontrado'}), 404

        db.session.delete(produto)
        db.session.commit()
        
        return jsonify({'mensagem': 'Produto deletado com sucesso'}), 200
    except Exception as e:
        return jsonify({'erro': f'Erro ao deletar produto: {str(e)}'}), 500
