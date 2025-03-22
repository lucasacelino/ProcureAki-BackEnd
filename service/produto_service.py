from flask import Blueprint, jsonify
from flask_restful import marshal, marshal_with, reqparse
from werkzeug.datastructures import FileStorage
import base64

from helpers.database import db
from models.Produto import Produto, produto_fields

produto_bp = Blueprint("produtos", __name__)

parser = reqparse.RequestParser()
parser.add_argument('nome', type=str, required=True, help="O campo 'nome' é obrigatório.")
parser.add_argument('preco', type=float, required=True, help="O campo 'preço' deve ser um número válido.")
parser.add_argument('quantidade', type=int, required=True, help="O campo 'quantidade' deve ser um número inteiro.")
# parser.add_argument('imagem_url', type=str, required=True, help="O campo 'imagem' é obrigatório.")
parser.add_argument('imagem_base64', type=FileStorage, location='files', required=True, help="Imagem do produto é obrigatória")
parser.add_argument('descricao', type=str, required=True, help="O campo 'descricao' é obrigatório.")
parser.add_argument('loja_id', type=int, required=True, help="O campo 'loja_id' é obrigatório e deve ser um número inteiro.")


@produto_bp.post("")
@marshal_with(produto_fields)
def criar_produto():
    try:
        dados = parser.parse_args()
        
        arquivo_imagem = dados['imagem_base64']
        if arquivo_imagem:
            imagem_base64 = base64.b64encode(arquivo_imagem.read()).decode('utf-8')
            # mime_type = arquivo_imagem.mimetype  # Opcional: salvar o tipo MIME
        else:
            return {'erro': 'Nenhuma imagem enviada'}, 400
        
        novo_produto = Produto(
            nome = dados['nome'],
            preco = dados['preco'],
            quantidade = dados['quantidade'],
            imagem_base64 = imagem_base64,
            descricao = dados['descricao'],
            loja_id = dados['loja_id']
        )

        db.session.add(novo_produto)
        db.session.commit()
        
        return novo_produto, 201
    
    except Exception as e:
        return jsonify({'erro': f'Erro ao criar produto: {str(e)}'}), 500


@produto_bp.get("")
@marshal_with(produto_fields)
def listar_produtos():
    try:
        produtos = Produto.query.all()
        return produtos, 200
    except Exception as e:
        return jsonify({'erro': f'Erro ao listar produtos: {str(e)}'}), 500


@produto_bp.get('<int:id>')
def buscar_produto(id):
    try:
        produto = Produto.query.get(id)
        if not produto:
            return {"mensagem": "Loja não encontrada"}, 404
        return marshal(produto, produto_fields), 200
    except Exception as e:
        return {'erro': f'Erro ao buscar produto: {str(e)}'}, 500


@produto_bp.put('/<int:id>')
def atualizar_produto(id):
    try:
        produto = Produto.query.get(id)
        if not produto:
            return {"mensagem": "produto não encontrado"}, 404

        dados = parser.parse_args()

        produto.nome = dados.get('nome', produto.nome)
        produto.preco = dados.get('preco', produto.preco)
        produto.quantidade = dados.get('quantidade', produto.quantidade)
        produto.imagem_base64 = dados.get('imagem_bas64', produto.imagem_url)
        produto.descricao = dados.get('descricao', produto.descricao)

        db.session.commit()
        return marshal(produto, produto_fields), 200
    
    except Exception as e:
        return jsonify({'erro': f'Erro ao atualizar produto: {str(e)}'}), 500


@produto_bp.delete('/<int:id>')
def deletar_produto(id):
    try:
        produto = Produto.query.get(id)
        if not produto:
            return {"mensagem": "produto não encontrado"}, 404

        db.session.delete(produto)
        db.session.commit()
        
        return jsonify({'mensagem': 'Produto deletado com sucesso'}), 200
    except Exception as e:
        return jsonify({'erro': f'Erro ao deletar produto: {str(e)}'}), 500
