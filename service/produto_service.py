from flask import Blueprint, jsonify
from flask_restful import marshal, marshal_with, reqparse
from werkzeug.utils import secure_filename
import requests

import os
from dotenv import load_dotenv

import cloudinary
import cloudinary.uploader
import cloudinary.api

from helpers.database import db
from helpers.logging import logger
from models.Produto import Produto, produto_fields

load_dotenv()
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

produto_bp = Blueprint("produtos", __name__)

UPLOAD_FOLDER = 'uploads' 
EXTENSOES_PERMITIDAS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in EXTENSOES_PERMITIDAS

parser = reqparse.RequestParser()
parser.add_argument('nome', type=str, required=True, help="O campo 'nome' é obrigatório.")
parser.add_argument('preco', type=float, required=True, help="O campo 'preço' deve ser um número válido.")
parser.add_argument('quantidade', type=int, required=True, help="O campo 'quantidade' deve ser um número inteiro.")
parser.add_argument('imagem_url', type=str, required=True, help="URL da imagem é obrigatória.")
parser.add_argument('descricao', type=str, required=True, help="O campo 'descricao' é obrigatório.")
parser.add_argument('loja_id', type=int, required=True, help="O campo 'loja_id' é obrigatório e deve ser um número inteiro.")


@produto_bp.post("")
@marshal_with(produto_fields)
def criar_produto():
    try:
        # dados = parser.parse_args()
        # imagem_url = dados['imagem_url']
        # print(imagem_url)
        # response = requests.get(imagem_url)
        # if response.status_code != 200:
        #     return {'erro': 'Não foi possível baixar a imagem'}, 400
        
        # filename = secure_filename(imagem_url.split('/')[-1].split('?')[0]) 
        # print(f"Nome do arquivo gerado: {filename}")
        # if not allowed_file(filename):
        #     return {'erro': 'Formato de imagem não permitido'}, 400

        # if not os.path.exists(UPLOAD_FOLDER):
        #     os.makedirs(UPLOAD_FOLDER)
        # filepath = os.path.join(UPLOAD_FOLDER, filename)
        # with open(filepath, 'wb') as f:
        #     f.write(response.content)
        
        dados = parser.parse_args()
        imagem_url = dados['imagem_url']
        print(imagem_url)
        response = requests.get(imagem_url)
        if response.status_code != 200:
            return {'erro': 'Não foi possível baixar a imagem'}, 400
        
        filename = secure_filename(imagem_url.split('/')[-1].split('?')[0]) 
        print(f"Nome do arquivo gerado: {filename}")
        if not allowed_file(filename):
            return {'erro': 'Formato de imagem não permitido'}, 400

        upload_result = cloudinary.uploader.upload(imagem_url)
        cloudinary_url = upload_result['secure_url']
        
        novo_produto = Produto(
            nome = dados['nome'],
            preco = dados['preco'],
            quantidade = dados['quantidade'],
            imagem_url = cloudinary_url,
            descricao = dados['descricao'],
            loja_id = dados['loja_id']
        )

        db.session.add(novo_produto)
        db.session.commit()
        
        logger.info("Produto criado com sucesso")
        return novo_produto, 201
    
    except Exception as e:
        logger.info("Erro ao criar produto:", str(e))
        return jsonify({'erro': f'Erro ao criar produto: {str(e)}'}), 500


@produto_bp.get("")
@marshal_with(produto_fields)
def listar_produtos():
    try:
        produtos = Produto.query.all()
        return produtos, 200
    
    except Exception as e:
        logger.error("Erro ao listar produtos")
        return jsonify({'erro': f'Erro ao listar produtos: {str(e)}'}), 500


@produto_bp.get('<int:id>')
def buscar_produto(id):
    try:
        produto = Produto.query.get(id)
        if not produto:
            logger.info(f"Produto não encontrado {produto}")
            return {"mensagem": "Loja não encontrada"}, 404
        return marshal(produto, produto_fields), 200
    
    except Exception as e:
        logger.error("Erro aao buscar produto")
        return {'erro': f'Erro ao buscar produto: {str(e)}'}, 500


@produto_bp.put('/<int:id>')
def atualizar_produto(id):
    try:
        produto = Produto.query.get(id)
        if not produto:
            logger.info(f"Produto não encontrado {produto}")
            return {"mensagem": "produto não encontrado"}, 404

        dados = parser.parse_args()

        produto.nome = dados.get('nome', produto.nome)
        produto.preco = dados.get('preco', produto.preco)
        produto.quantidade = dados.get('quantidade', produto.quantidade)
        produto.imagem_url = dados.get('imagem_url', produto.imagem_url)
        produto.descricao = dados.get('descricao', produto.descricao)

        db.session.commit()
        return marshal(produto, produto_fields), 200
    
    except Exception as e:
        logger.info(f"Erro ao atualizar produto {e}")
        return jsonify({'erro': f'Erro ao atualizar produto: {str(e)}'}), 500


@produto_bp.delete('/<int:id>')
def deletar_produto(id):
    try:
        produto = Produto.query.get(id)
        if not produto:
            logger.info(f"Produto não encontrado {produto}")
            return {"mensagem": "produto não encontrado"}, 404

        db.session.delete(produto)
        db.session.commit()
        
        return jsonify({'mensagem': 'Produto deletado com sucesso'}), 200
    
    except Exception as e:
        logger.info(f"Produto não encontrado {produto}")
        return jsonify({'erro': f'Erro ao deletar produto: {str(e)}'}), 500
