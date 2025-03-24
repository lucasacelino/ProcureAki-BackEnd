from helpers.database import db
from helpers.application import app
from helpers.database import migrate
from helpers.cors import cors

from service.loja_service import loja_bp
from service.produto_service import produto_bp
from service.categoria_service import categorias_bp

app.config.from_object("config")

cors.init_app(app)
db.init_app(app)
migrate.init_app(app, db)

with app.app_context():
    db.create_all()

app.register_blueprint(loja_bp, url_prefix="/lojas")
app.register_blueprint(produto_bp, url_prefix="/produtos")
app.register_blueprint(categorias_bp, url_prefix="/categorias")

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

if __name__ == "__main__":
    app.run(debug=True)
