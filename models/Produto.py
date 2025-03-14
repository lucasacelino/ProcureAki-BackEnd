from helpers.database import db

class Produto(db.Model):
    __tablename__ = "tb_produtos"
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Integer, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    imagem_url = db.Column(db.String(100), nullable=False)
    descricao =  db.Column(db.String(300), nullable=False)
