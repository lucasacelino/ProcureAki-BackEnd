from flask import Flask
from helpers.database import db
from service.loja_service import loja_bp

app = Flask(__name__)
app.config.from_object("config")

db.init_app(app)

with app.app_context():
    db.create_all()
    print("Banco de dados e tabelas criados com sucesso!")

app.register_blueprint(loja_bp, url_prefix="/lojas")

if __name__ == "__main__":
    app.run(debug=True)
